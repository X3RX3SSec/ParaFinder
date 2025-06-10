# 🕷️ X3RX3S's Parameter Finder

> A multithreaded, blazing-fast URL parameter discovery tool for recon ninjas.  
> Built for speed, stealth, and sexy terminal vibes.  
> Made by **X3RX3S** — use non responsibly 💀

---

## What is this?

**X3RX3S's Parameter Finder** is a CLI tool that crawls a website and identifies URLs containing common GET parameters. It uses threading for speed, optional user-agent rotation for stealth, supports proxies and cookies, and can output results in TXT, CSV, or JSON formats.

This is for **bug bounty hunters**, **pentesters**, or anyone doing **web app recon** who wants to quickly gather parameterized URLs for fuzzing, testing, or exploitation.

---

## Features

- > Multi-threaded crawling
- > Finds **40 (default)** or **100+ (supreme)** common parameters
- > Terminal-friendly **light blue output**
- > Optional **User-Agent randomization**
- > **Proxy** support (`http`, `https`)
- > **Custom cookies** for authenticated crawling
- > **Crawl depth** control
- > Output in **TXT**, **CSV**, or **JSON**
- > Clean, lean, and fast as fxck.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/X3RX3SSec/ParaFinder.git
cd ParaFinder 
pip install requests beautifulsoup4 tqdm
```

---

## Usage

```bash
python3 parafinder.py -h
python parafinder.py <URL> [options]
```

### Options

| Option                | Description                                                                 | Default       |
|----------------------|-----------------------------------------------------------------------------|---------------|
| `--mode`             | Parameter mode: `default` (40) or `supreme` (100+)                          | `default`     |
| `--threads`          | Number of threads to use for crawling                                       | `10`          |
| `--user-agent-random`| Randomizes the `User-Agent` header for each request                         | Off           |
| `--output-file`      | Save results to a file                                                      | None          |
| `--output-format`    | File format: `txt`, `json`, or `csv`                                        | `txt`         |
| `--proxy`            | Use a proxy (e.g., `http://127.0.0.1:8080`)                                 | None          |
| `--cookie`           | Send cookies (e.g., `"PHPSESSID=abc123;"`)                                  | None          |
| `--depth`            | How deep to crawl: `1` (just homepage links), `2` (links of links), etc     | `2`           |

---

## Examples

### Crawl with defaults:

```bash
python parafinder.py https://example.com
```

### Use supreme mode and random user-agent:

```bash
python parafinder.py https://example.com --mode supreme --user-agent-random
```

### Save to JSON file:

```bash
python parafinder.py https://example.com --output-file out.json --output-format json
```

### Use proxy, cookies, and crawl depth 3:

```bash
python paramfinder.py https://target.com \
  --proxy http://127.0.0.1:8080 \
  --cookie "auth=token123" \
  --depth 3
```

---

## Output

Results are printed in **light blue** in your terminal and can be saved as:

- `results.txt`
- `results.csv`
- `results.json`

Each file will contain only the URLs where at least **one common parameter** was detected.

---

## ⚠️ Legal Notice

This tool is intended for **authorized testing, learning, and bug bounty** purposes only.  
Do **NOT** use it on domains you don't own or have explicit permission to test. Not that anyone would listen to this 🤐

You are responsible for your actions. I take no liability for misuse.

---

## 🧠 Tips

- Pipe output into other tools like `ffuf`, `xargs`, or `wfuzz`
- Combine with your own wordlists by modifying the `default_params` and `supreme_params` arrays
- Try crawling authenticated areas using `--cookie`
- Use `--depth 1` for fast shallow scans, `--depth 3+` for deeper crawls

---

## 🤘 Author

**X3RX3S**

Drop a ⭐ if this helped your recon flow.  
PRs welcome if you wanna contribute!

---
