# NetScope

NetScope is a lightweight **web enumeration & reconnaissance** tool for pentesters, bug bounty hunters, and security researchers.  
It focuses on fast, actionable results and gives you flexible proxy automation so you can test through proxies you control.

**Core features**
- Directory & file enumeration (wordlist fuzzing)  
- Subdomain discovery  
- Tech stack detection & basic banner grabbing  
- Proxy automation: spawn local HTTP proxies or start remote proxies via SSH  
- Proxy-aware port scanner supporting `http`, `socks4`, `socks5` (client via `PySocks`)  
- Modular design — add modules under `Web_recon/` or `NetRecon/`

---

- [Quick setup](#quick-setup)

---

## Quick setup

Clone and prepare environment:

```bash
git clone https://github.com/digitalpardoxxoo/Netscope.git
cd Netscope
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt

