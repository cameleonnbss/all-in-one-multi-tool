# 🛠️ ALL IN ONE TOOL V5

> All-In-One Hacking Toolkit — two versions available, actively in development.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![License](https://img.shields.io/badge/License-Educational%20Only-red)

---

## 🚧 Work In Progress

This project is **not finished yet**. Some modules may be broken, incomplete or untested.  
Known issues are listed below.

---

## ⚡ Quick Start

Two versions are available on this repo.

### v3.0 — Stable (recommended)
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tool.py
```

### v5.0 — Latest (in development)
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tooV5.py
```

> Missing dependencies (`requests`, `colorama`, `dnspython`) are auto-installed on first run.

---

## 📦 Python Dependencies

| Package          | Purpose                  |
|------------------|--------------------------|
| `requests`       | HTTP requests / APIs     |
| `colorama`       | Terminal colors          |
| `beautifulsoup4` | HTML parsing             |
| `dnspython`      | DNS resolution           |
| `anthropic`      | AI Chatbot (optional)    |

---

## 🗂️ Modules — v5.0

| # | Name | Status |
|---|------|--------|
| 01 | DDoS Flood — UDP, SYN, HTTP, Slowloris | ✅ Working |
| 02 | OSINT — email, phone, username | ⚠️ Partially broken |
| 03 | XSS Injector — 25+ payloads | ✅ Working |
| 04 | SQL Injector — error-based & time-based | ✅ Working |
| 05 | Brute Force — SSH, FTP, HTTP Auth | ✅ Working |
| 06 | Vulnerability Scanner — headers, SSL, endpoints | ✅ Working |
| 07 | Network Scanner — ping sweep, OS fingerprint | ✅ Working |
| 08 | Port Scanner — 25 common ports + banner grab | ✅ Working |
| 09 | DNS Enumeration — A, MX, NS, TXT, subdomains | ✅ Working |
| 10 | Hash & Encode — MD5/SHA/NTLM + Base64/Hex | ✅ Working |
| 11 | Crypto Tools — hash identifier, ROT13, URL encode | ✅ Working |
| 12 | AI Chatbot — Claude API / offline fallback | ✅ Working |
| 13 | Social Media Tools — username on 50+ platforms | ⚠️ Some platforms blocked |
| 14 | Web Hacking Suite — dir buster, admin finder | ✅ Working |
| 15 | Phishing Tools — ZPhisher integration | ⚠️ Linux only |
| 16 | Reverse Shell Generator — 13 languages | ✅ Working |
| 17 | WiFi Tools — aircrack-ng suite | ⚠️ Linux only |
| 18 | Metasploit Helper — msfvenom commands | ✅ Working |

---

## 🗂️ Modules — v3.0

| # | Category | Tools |
|---|----------|-------|
| 1 | Bruteforce | Instagram · SSH · FTP · RDP · Zip · PDF |
| 2 | OSINT | Sherlock · Phone · Email · IP · Subdomains · Maigret |
| 3 | Phishing | ZPhisher · CamPhish · HiddenEye · ShellPhish |
| 4 | DDoS | Layer4 Flood · Slowloris · HULK · LOIC Clone |
| 5 | WiFi | Scanner · Handshake · Deauth · WPS · MAC Changer |
| 6 | Web Hacking | Nmap · SQLmap · Gobuster · Nikto · XSStrike |
| 7 | Social Media | Report tools (IG, TikTok, Snap, FB) |
| 8 | AI Chatbot | OpenRouter / DeepSeek model |
| 9 | Network Tools | Ping · DNS · Traceroute · Headers · Port scan |
| 10 | Crypto | Hash gen · Base64 · Caesar · Password gen |
| 11 | Utilities | System info · Public IP · Whois |
| 12 | Download All | Batch clone all tool repos |
| 13 | Bonus | Simulated stubs (educational reference) |

---

## ⚠️ Known Issues

- **OSINT module (v5)** — some checks are not working correctly at the moment (phone lookup, certain APIs unreachable). Fix in progress.
- **Social Media Tools** — several platforms actively block automated requests, results may vary.
- **WiFi & Phishing modules** — Linux only, will not work on Windows without WSL.

---

## 🖥️ Compatibility

| Feature                  | Linux | Windows | macOS |
|--------------------------|:-----:|:-------:|:-----:|
| Core menu & modules      | ✅    | ✅      | ✅    |
| WiFi (aircrack-ng)       | ✅    | ❌ WSL  | ⚠️    |
| Port / Network Scanner   | ✅    | ✅      | ✅    |
| Reverse Shell Generator  | ✅    | ✅      | ✅    |
| Brute Force SSH/FTP      | ✅    | ✅      | ✅    |

---

## 👤 Author

**cameleonnbss**

- 💬 Discord : `cameleonmortis`
- 🐙 GitHub : [github.com/cameleonnbss](https://github.com/cameleonnbss)
