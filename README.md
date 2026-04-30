# 🛠️ ALL IN ONE TOOL

> All-In-One Hacking Toolkit — two versions available, actively in development.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-lightgrey)
![Modules](https://img.shields.io/badge/Modules-33-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![License](https://img.shields.io/badge/License-Educational%20Only-red)

---

## 🚧 Work In Progress

This project is **not finished yet**. Some modules may be broken, incomplete or untested.
Known issues are listed below.

---

## ⚡ Quick Start

Two versions are available on this repo.

### v3.0 — Stable
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tool.py
```

### v5.0 — Latest (33 modules)
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tooV5.py
```

> Missing dependencies are auto-installed on first run if you skip the `pip install` step.

---

## 📦 Python Dependencies

All dependencies live in `requirements.txt`.

| Package          | Purpose                                           |
|------------------|---------------------------------------------------|
| `requests`       | HTTP requests / API calls                         |
| `colorama`       | Terminal colors (cross-platform)                  |
| `beautifulsoup4` | HTML parsing (OSINT, TechInt)                     |
| `dnspython`      | DNS resolution (MX / SPF / subdomain enum)        |
| `Pillow`         | Image metadata, steganography, EXIF               |
| `phonenumbers`   | Phone lookup — country / carrier / timezone      |
| `cryptography`   | AES-256 encryption, RSA keygen                    |
| `paramiko`       | SSH brute force                                   |
| `pymysql`        | MySQL brute force                                 |
| `impacket`       | SMB brute force                                   |
| `scapy`          | Packet sniffer, ARP spoofer (requires root)       |

### System tools (not pip-installable)

| Tool                   | Install                           | Used by                     |
|------------------------|-----------------------------------|-----------------------------|
| `msfvenom` / `msfconsole` | Metasploit Framework           | Payload Generator (24)      |
| `xfreerdp`             | `sudo apt install freerdp2-x11`   | RDP brute force             |
| `aircrack-ng` suite    | `sudo apt install aircrack-ng`    | WiFi Tools (17)             |
| `traceroute`, `whois`  | `sudo apt install traceroute whois` | Network Scanner          |

---

## 🗂️ Modules — v5.0 (33 total)

### Attack & Exploit
| #  | Name | Status |
|----|------|--------|
| 01 | DDoS Flood — UDP / SYN / HTTP / Slowloris | ✅ Working |
| 03 | XSS Injector — 20+ payloads | ✅ Working |
| 04 | SQL Injector — error & time based | ✅ Working |
| 05 | Brute Force — SSH · FTP · HTTP · WordPress · SMB · MySQL · RDP | ✅ Working |
| 25 | ARP Spoofer — MITM Layer 2 | ⚠️ Root + Linux |
| 28 | XXE Injection — 7 payloads incl. Billion Laughs | ✅ Working |
| 29 | SSRF Scanner — AWS/GCP metadata probes | ✅ Working |

### Reconnaissance & Scanning
| #  | Name | Status |
|----|------|--------|
| 02 | OSINT — email · phone · username · Google dorks | ✅ Working |
| 06 | Vulnerability Scanner — headers, SSL, CORS, cookies, .git | ✅ Working |
| 07 | Network Scanner — ping/ARP sweep, traceroute, whois, geoip | ✅ Working |
| 08 | Port Scanner — 25 ports + banner grab | ✅ Working |
| 09 | DNS Enumeration — A/MX/NS/TXT/subdomains | ✅ Working |
| 21 | Subdomain Takeover — 13 providers | ✅ Working |
| 22 | Shodan Search — query + host info | ✅ Working |
| 26 | CVE Scanner — NVD API + auto banner lookup | ✅ Working |
| 29 | SSRF Scanner | ✅ Working |
| 30 | Packet Sniffer — HTTP creds / DNS / general | ⚠️ Root + Linux |
| 32 | TechInt Analyzer — stack fingerprinting | ✅ Working |

### Crypto & Forensics
| #  | Name | Status |
|----|------|--------|
| 10 | Hash & Encode — MD5/SHA/NTLM + Base64/Hex | ✅ Working |
| 11 | Crypto Tools — AES-256, RSA, Caesar brute, HMAC, XOR | ✅ Working |
| 19 | Steganography — LSB hide/extract, strings | ✅ Working |
| 20 | JWT Tool — decode, none-alg, brute HS256 | ✅ Working |
| 23 | File Analyzer — magic bytes, hashes, entropy | ✅ Working |
| 31 | Image Metadata — full EXIF + GPS → Google Maps | ✅ Working |

### Offensive tooling
| #  | Name | Status |
|----|------|--------|
| 14 | Web Hacking Suite — directory buster | ✅ Working |
| 15 | Phishing Tools — ZPhisher integration | ⚠️ Linux only |
| 16 | Reverse Shell Generator — 14 langs + TTY upgrade guide | ✅ Working |
| 17 | WiFi Tools — aircrack-ng suite | ⚠️ Linux + WiFi adapter |
| 18 | Metasploit Helper — msfvenom cheatsheet | ✅ Working |
| 24 | Payload Generator — msfvenom wrapper + XOR / PS base64 | ✅ Working |
| 27 | Wordlist Generator — leet-speak + year mutations | ✅ Working |

### Intel / OSINT
| #  | Name | Status |
|----|------|--------|
| 13 | Social Media Tools — 50+ platforms | ⚠️ Some platforms block |
| 33 | Phone Lookup — country, carrier, WhatsApp/Telegram probe | ✅ Working |

### Misc
| #  | Name | Status |
|----|------|--------|
| 12 | AI Chatbot — 10 models via OpenRouter + streaming | ✅ Working |

---

## 🤖 AI Chatbot (module 12)

Multi-model chat with streaming output. Supported models:

- **DeepSeek Chat / DeepSeek R1** (reasoning)
- **Claude Sonnet 4.5 / Opus 4.1**
- **GPT-4o / GPT-4o Mini**
- **Gemini 2.0 Flash** (free tier)
- **Llama 3.3 70B**, **Qwen 2.5 Coder 32B**, **Mistral Large**

### Setup

1. Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys)
2. Launch module 12 → it asks for the key on first run
3. Key is saved to `~/AllInOneTool/tools/.openrouter_key` (chmod 600)

### In-chat commands

| Command      | Action                                        |
|--------------|-----------------------------------------------|
| `/model`     | Switch model (numbered list)                  |
| `/style`     | Switch style: hacker / explain / coder / ctf  |
| `/clear`     | Reset conversation history                    |
| `/history`   | Show conversation so far                      |
| `/save`      | Save chat to markdown file                    |
| `/exit`      | Back to main menu                             |

---

## ⚠️ Known Issues

- **Social Media Tools (13)** — several platforms actively block automated requests.
- **WiFi, ARP Spoof, Packet Sniff** — require root + Linux.
- **Phishing (15)** — Linux only, needs `git`.
- **Windows** — some modules rely on Unix-only commands (`ping -c`, `traceroute`). Use WSL for full compatibility.

---

## 🖥️ Compatibility

| Feature                  | Linux | Windows | macOS | Termux |
|--------------------------|:-----:|:-------:|:-----:|:------:|
| Core menu & modules      | ✅    | ✅      | ✅    | ✅     |
| WiFi (aircrack-ng)       | ✅    | ❌ WSL  | ⚠️    | ❌     |
| Port / Network Scanner   | ✅    | ✅      | ✅    | ✅     |
| Reverse Shell Generator  | ✅    | ✅      | ✅    | ✅     |
| Brute Force SSH/FTP      | ✅    | ✅      | ✅    | ✅     |
| ARP Spoof / Sniffer      | ✅    | ❌      | ⚠️    | ❌     |
| AI Chatbot               | ✅    | ✅      | ✅    | ✅     |
| Image Metadata / EXIF    | ✅    | ✅      | ✅    | ✅     |

### Termux install

```bash
pkg update && pkg upgrade
pkg install python python-pip git openssh nmap whois traceroute
pip install -r requirements.txt
python multi-tooV5-fixed.py
```

Raw-socket modules (**17, 25, 30**) will not run on Termux without root.

---

## 👤 Author

**cameleonnbss**

- 💬 Discord : `cameleonmortis`
- 🐙 GitHub : [github.com/cameleonnbss](https://github.com/cameleonnbss)

---

## ⚖️ Disclaimer

This toolkit is provided **for educational purposes, authorized penetration testing, and CTF challenges only**. The author is **NOT responsible** for any misuse. Only run it against systems you own or are explicitly authorized to test.

