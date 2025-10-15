# 🚀 NetScope
**Recon. Fast. No BS.** Port scanning, web enumeration, proxy automation—all in one tool.

[![Status](https://img.shields.io/badge/status-beta-yellow.svg)]() [![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

---

## ⚡ What It Does

Port scanning + banner grabbing + directory fuzzing + subdomain enumeration + proxy routing. Everything you need, nothing you don't.

---

## 📦 Install

```bash
git clone https://github.com/digitalpardoxxoo/Netscope.git && cd Netscope
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && python main.py
```

---

## 🎮 Three Modes

**🎯 Mode 1: Direct Scan**
```
Choice: 1 → Ports: 80,443,22 → Host: target.com → Delay: 1
```
Opens ports, grabs banners. Done.

**🕷️ Mode 2: Web Recon**
```
Choice: 2 → crawl/fuzz/sub_enum → URL/Domain + Wordlist
```
Crawl sites, fuzz directories, hunt subdomains.

**👻 Mode 3: Proxy Scan**
```
Choice: 3 → Same as Mode 1 but routed through your proxy
```
Stay stealthy. Distribute requests.

---

## ⚙️ Config

**Add proxies** in `NetRecon/net_scan.py`:
```python
PROXIES = [
    {"type": "http", "addr": "127.0.0.1", "port": 8000},
    {"type": "socks5", "addr": "127.0.0.1", "port": 1080},
]
```

**Use wordlists:** Grab from [SecLists](https://github.com/danielmiessler/SecLists) or make your own.

---

## 🧩 Extend

Drop new modules in `Web_recon/` or `NetRecon/`, import in `main.py`. Build what you need.

---

## ⚠️ Permission First

Authorized testing only. Get written permission. Always.

---

**Happy hunting.** 🎯
