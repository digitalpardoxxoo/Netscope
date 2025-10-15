# 🚀 NetScope

**NetScope** — lightweight web enumeration & reconnaissance tool with optional proxy automation (local & remote), proxy-aware port scanning, and easy extension points.  
Built for pentesters, bug bounty hunters, and security researchers who want results fast and control over their testing environment.

---

[![Status](https://img.shields.io/badge/status-beta-yellow.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

---

## 🔎 What it does (TL;DR)
- Directory & file enumeration (wordlist fuzzing)  
- Subdomain discovery  
- Tech stack detection & simple banner grabbing  
- Proxy automation:
  - Generate **local** HTTP proxies for quick testing
  - Bootstrap **remote** proxies on VPSes you control via SSH
  - Use proxies (HTTP / SOCKS4 / SOCKS5) with the port scanner
- Modular: add new recon modules under `Web_recon/` or `NetRecon/`

---

## ⚙️ Design goals
- **Practical**: tools that actually help you map attack surface quickly.  
- **Safe-by-default**: local proxies used unless you explicitly spawn remote ones.  
- **Modular**: easy to extend and slot new recon features.  
- **Beginner-friendly**: guided CLI, minimal setup.

---

## 📦 Quick install (3 steps)
```bash
git clone https://github.com/digitalpardoxxoo/Netscope.git
cd Netscope
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt  # or install pieces below individually
