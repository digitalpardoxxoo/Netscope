# 🚀 NetScope
**Lightweight web enumeration & reconnaissance tool for pentesters, bug bounty hunters, and security researchers.**

[![Status](https://img.shields.io/badge/status-beta-yellow.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.7%2B-green.svg)]()

---

## ⚡ What It Does

NetScope is a modular reconnaissance toolkit that combines network scanning, web enumeration, and proxy automation into one streamlined tool. Get fast results with full control over your testing environment.

- **Port Scanning** — TCP connect scans with banner grabbing (HTTP, HTTPS, FTP, SSH, etc.)
- **Directory Fuzzing** — Wordlist-based directory discovery
- **Subdomain Enumeration** — Find subdomains from wordlists
- **Web Crawling** — Fetch and parse site structure, links, and metadata
- **Proxy Support** — Local HTTP proxy creation + proxy-aware port scanning
- **Modular Design** — Easy to extend with custom recon modules

---

## 📋 Requirements

- Python 3.7+
- requests
- beautifulsoup4

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/digitalpardoxxoo/Netscope.git
cd Netscope

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\Activate.ps1     # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Quick Start

```bash
python main.py
```

You'll see a menu:

```
Choose an option:
1 - Network Scan
2 - Web Recon
3 - Network Scan via Proxy
```

---

## 💻 Usage Guide

### 1️⃣ Network Scan (Direct)

Scan ports on a target host with automatic banner grabbing.

```
Choice: 1
Enter Ports: 22,80,443,3306,8080
Enter Host: example.com
Enter Delay (seconds): 1
```

**What happens:**
- Scans each port sequentially
- Attempts banner grabbing on open ports
- Displays service fingerprints (HTTP, HTTPS, FTP, SSH, etc.)
- Shows connection status and timing

---

### 2️⃣ Web Recon

Choose from three web-based reconnaissance modes.

#### **Web Crawling**
```
Choice: 2
Command: crawl
Enter URL: https://example.com
```
Fetches page content, extracts title, and lists all links.

#### **Directory Fuzzing**
```
Choice: 2
Command: fuzz
Enter URL: https://example.com
Enter Wordlist: wordlists/dirs.txt
```
Tests each path from your wordlist. Reports status codes 200 and 403.

#### **Subdomain Enumeration**
```
Choice: 2
Command: sub_enum
Enter Domain: example.com
Enter Wordlist: wordlists/subs.txt
```
Brute-forces subdomains and reports live ones (200, 301, 302, 403, 404).

---

### 3️⃣ Network Scan via Proxy

Route your port scans through a local or remote proxy.

```
Choice: 3
Enter Ports: 80,443
Enter Host: example.com
Enter Delay: 1

Available proxies:
0 - {'type': 'http', 'addr': '127.0.0.1', 'port': 8000}
1 - {'type': 'socks5', 'addr': '127.0.0.1', 'port': 1080}
...
Select proxy index (-1 for direct): 0
```

Useful for:
- Testing from multiple IPs
- Bypassing simple rate limits
- Lab testing with local proxies

---

## ⚙️ Configuration

### Modify Proxy List

Edit `NetRecon/net_scan.py` to customize proxies:

```python
class Port_scanner:
    PROXIES = [
        {"type": "http",  "addr": "127.0.0.1", "port": 8000},
        {"type": "http",  "addr": "127.0.0.1", "port": 8001},
        {"type": "socks5", "addr": "127.0.0.1", "port": 1080},
        {"type": "socks4", "addr": "127.0.0.1", "port": 1081},
    ]
```

### Wordlists

Create your own or use community lists:
- `wordlists/dirs.txt` — Common directories
- `wordlists/subs.txt` — Common subdomains

---

## 🧩 Module Overview

### `NetRecon/net_scan.py`

**`Port_scanner` class**
- `scan(port)` — Scan single port with banner grab
- `run(chunk_size=5, max_workers=4)` — Threaded scan of port list
- Banner grabbing for: HTTP, HTTPS, FTP, SSH

### `Web_recon/Web_enum.py`

**`Web_rec` class**
- `fetch_url(url)` — Crawl and parse HTML
- `DirectoryFuzz(url, wordlist)` — Fuzz directories
- `Subdomain_enum(domain, wordlist)` — Enumerate subdomains

---

## 🔌 Proxy Modes

### Local HTTP Proxy
Use `ProxyMaker` to spawn N local HTTP proxies:

```python
from NetRecon.net_scan import ProxyMaker

pm = ProxyMaker(start_port=8000, count=5)
pm.start_all()  # Starts proxies on 8000-8004
# ... run your scans ...
pm.stop_all()
```

### Setup with SSH Tunnel
Create SOCKS5 proxy via SSH:

```bash
ssh -D 1080 user@your_vps
# Now use 127.0.0.1:1080 as SOCKS5 proxy in NetScope
```

---

## 🛠️ Extending NetScope

### Add Custom Recon Module

Create a new file under `Web_recon/` or `NetRecon/`:

```python
# Web_recon/custom_module.py
class CustomRecon:
    def __init__(self, target):
        self.target = target
    
    def run(self):
        # Your logic here
        pass
```

Then import and use in `main.py`:

```python
from Web_recon.custom_module import CustomRecon

# Add option in web_scrape() or main menu
```

---

## 📊 Output Examples

### Port Scan
```
Connection Established on Port 80
HTTP Banner from port 80:
HTTP/1.1 200 OK
Server: Apache/2.4.41
...

Connection Established on Port 443
HTTPS Banner from port 443:
HTTP/1.1 200 OK
Server: nginx/1.18.0
...
```

### Directory Fuzzing
```
Found:https://example.com/admin , (Status:200)
Found:https://example.com/login , (Status:200)
Found:https://example.com/config , (Status:403)
```

### Subdomain Enumeration
```
Found:https://api.example.com,(Status:200)
Found:https://dev.example.com,(Status:301)
Found:https://mail.example.com,(Status:403)
```

---

## ⚠️ Safety & Ethics

- **Always get written permission** before scanning targets you don't own
- NetScope is designed for authorized security testing only
- Misuse may violate laws — use responsibly
- Default behavior is safe: local proxies only, no TOR/VPN unless configured

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No such file or directory" (wordlist) | Verify wordlist path exists |
| Connection timeout | Increase delay, check target reachability |
| "Invalid input" | Enter comma-separated ports (e.g., `80,443,22`) |
| Proxy not connecting | Verify proxy is running and address is correct |
| SSL/certificate errors | Normal for self-signed certs; check banner output |

---

## 📝 Wordlist Resources

- **SecLists** — https://github.com/danielmiessler/SecLists
- **Seclists dirs** — `SecLists/Discovery/Web-Content/`
- **Seclists subdomains** — `SecLists/Discovery/DNS/`

---

## 📄 License

MIT License — See LICENSE file for details

---

## 🤝 Contributing

Found a bug? Have an idea? Submit issues or PRs to improve NetScope.

---

## ⚡ Tips & Tricks

- **Reduce scanning time:** Increase `max_workers` (default 4)
- **Stealth scanning:** Use proxies to distribute requests
- **Custom banners:** Modify `Port_scanner.scan()` for specific services
- **Batch jobs:** Create a script to loop through multiple targets

---

**Happy hacking! 🎯**
