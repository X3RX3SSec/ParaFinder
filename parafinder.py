import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from queue import Queue
import threading
import random
import argparse
import json
import csv
import sys
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()

GREEN = "\033[92m"
PURPLE = "\033[95m"
BLUE = "\033[94m"
RESET = "\033[0m"

visited = set()
queue = Queue()
found_urls = set()
lock = threading.Lock()
progress = None

default_params = [
    "id", "page", "p", "cat", "category", "dir", "action", "folder", "file",
    "search", "query", "url", "ref", "referrer", "image", "img", "u", "user",
    "username", "profile", "site", "type", "lang", "keyword", "key", "token",
    "menu", "module", "option", "view", "layout", "task", "item", "news",
    "show", "content", "article", "detail", "s", "name"
]

supreme_params = default_params + [
    "doc", "document", "folderid", "download", "feed", "format", "mode", "redir",
    "redirect", "fileid", "imgid", "video", "mp4", "src", "next", "prev", "list",
    "data", "input", "callback", "debug", "var", "cmd", "exec", "run", "include",
    "dest", "destination", "loc", "location", "path", "link", "target", "from",
    "goto", "out", "back", "home", "return", "form", "submit", "object", "load",
    "res", "resource", "embed", "style", "theme", "temp", "template", "actionid",
    "downloadid", "get", "set", "config", "controller", "filter", "section",
    "optionid", "channel", "instance", "win", "frame", "screen", "context",
    "track", "auth", "authentication", "admin", "panel", "dashboard"
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
]

def print_banner():
    lines = [
        " _______  _______  ______    _______  _______  ___   __    _  ______   _______  ______   ",
        "|       ||   _   ||    _ |  |   _   ||       ||   | |  |  | ||      | |       ||    _ |  ",
        "|    _  ||  |_|  ||   | ||  |  |_|  ||    ___||   | |   |_| ||  _    ||    ___||   | ||  ",
        "|   |_| ||       ||   |_||_ |       ||   |___ |   | |       || | |   ||   |___ |   |_||_ ",
        "|    ___||       ||    __  ||       ||    ___||   | |  _    || |_|   ||    ___||    __  |",
        "|   |    |   _   ||   |  | ||   _   ||   |    |   | | | |   ||       ||   |___ |   |  | |",
        "|___|    |__| |__||___|  |_||__| |__||___|    |___| |_|  |__||______| |_______||__| |__| ",
        "                                       by X3RX3S"
    ]
    for i, line in enumerate(lines):
        color = GREEN if i % 2 == 0 else PURPLE
        print(color + line + RESET)

def get_links(url, headers, proxies, depth):
    if depth <= 0:
        return
    try:
        resp = requests.get(url, headers=headers, timeout=5, proxies=proxies, verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup.find_all('a', href=True):
            link = urljoin(url, tag['href'])
            yield link
    except Exception:
        return

def scan_url(url, params):
    parsed = urlparse(url)
    if parsed.query:
        for param in params:
            if f"{param}=" in parsed.query:
                with lock:
                    found_urls.add(url)
                break

def worker(params, user_agent_random, proxies, cookies):
    while not queue.empty():
        url, depth = queue.get()
        if url in visited:
            queue.task_done()
            continue
        visited.add(url)
        headers = {
            'User-Agent': random.choice(user_agents) if user_agent_random else user_agents[0]
        }
        if cookies:
            headers['Cookie'] = cookies
        scan_url(url, params)
        for link in get_links(url, headers, proxies, depth):
            if link not in visited:
                queue.put((link, depth - 1))
        queue.task_done()
        if progress:
            progress.update(1)

def crawl(start_url, mode="default", user_agent_random=False, threads=10, proxy=None, cookies=None, depth=2):
    params = default_params if mode == "default" else supreme_params
    proxies = {"http": proxy, "https": proxy} if proxy else None
    queue.put((start_url, depth))
    global progress
    progress = tqdm(total=1000, desc="Crawling", unit="url")
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(params, user_agent_random, proxies, cookies))
        t.daemon = True
        t.start()
    queue.join()
    progress.close()
    return sorted(found_urls)

def save_output(results, filename, fmt):
    if not filename:
        return
    try:
        if fmt == "txt":
            with open(filename, "w") as f:
                for url in results:
                    f.write(url + "\n")
        elif fmt == "json":
            with open(filename, "w") as f:
                json.dump(list(results), f, indent=2)
        elif fmt == "csv":
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["URL"])
                for url in results:
                    writer.writerow([url])
        print(f"{PURPLE}[+] Results saved to {filename}{RESET}")
    except Exception as e:
        print(f"[!] Error saving file: {e}")

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(
        description="Multi-threaded Parameter Finder by X3RX3S",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("url", help="Target URL to begin crawling")
    parser.add_argument("--mode", choices=["default", "supreme"], default="default", help="Crawl with 40 or 100+ common GET parameters")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use")
    parser.add_argument("--user-agent-random", action="store_true", help="Randomize User-Agent header per request")
    parser.add_argument("--output-file", help="File to save results")
    parser.add_argument("--output-format", choices=["txt", "json", "csv"], default="txt", help="Format for saved output")
    parser.add_argument("--proxy", help="Proxy server (http://ip:port or https://ip:port)")
    parser.add_argument("--cookie", help="Cookie header string for authenticated crawling")
    parser.add_argument("--depth", type=int, default=2, help="Crawl depth (e.g. 1 = only links from start URL, 2 = links of links, etc)")

    args = parser.parse_args()
    results = crawl(
        args.url,
        args.mode,
        args.user_agent_random,
        args.threads,
        args.proxy,
        args.cookie,
        args.depth
    )

    print(f"\n{GREEN}[+] Found {len(results)} parameterized URLs:{RESET}")
    for r in results:
        print(f"{BLUE}{r}{RESET}")

    save_output(results, args.output_file, args.output_format)

