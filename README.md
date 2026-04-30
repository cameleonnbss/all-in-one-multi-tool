# 🛠️ ALL IN ONE TOOL

> All-In-One Hacking Toolkit — 40 modules, 2 versions, actively developed.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-lightgrey)
![Modules](https://img.shields.io/badge/Modules-40-green)
![AI](https://img.shields.io/badge/AI-Uncensored-red)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![License](https://img.shields.io/badge/License-Educational%20Only-red)

---

## 🚧 Work In Progress

Some modules may still be rough around the edges — feedback welcome.

---

## ⚡ Quick Start

### v5.0 — Latest (40 modules)
Voici une version adaptée et propre des instructions d’installation selon l’OS :

---

# 🛠️ Installation – ALL IN ONE TOOL

## ⚡ Prérequis (tous systèmes)

* Python 3 installé
* pip installé
* Git installé

---

# 🐧 Linux (Ubuntu / Debian / Kali)

```bash
sudo apt update && sudo apt install git python3 python3-pip -y

git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool

pip3 install -r requirements.txt --break-system-packages

python3 multi-tooV5.py
```

or make a venv :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


# 🍎 macOS

```bash
brew install git python

git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python3 multi-tooV5.py
```

---

# 🪟 Windows (PowerShell)

```powershell
winget install Git.Git
winget install Python.Python.3

git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python multi-tooV5.py
```

---

# 📱 Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install git python -y

git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool

pip install -r requirements.txt

python multi-tooV5.py
```


### v3.0 — Stable
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tool.py
```

> Missing deps are auto-installed on first run if you skip `pip install`.

---

## 📦 Dependencies

All pip dependencies sit in `requirements.txt`:

```
requests, colorama, beautifulsoup4, dnspython, Pillow,
phonenumbers, cryptography, paramiko, pymysql, impacket, scapy
```

### System tools (not pip-installable)

| Tool                   | Install                           | Used by                     |
|------------------------|-----------------------------------|-----------------------------|
| `msfvenom`             | Metasploit Framework              | Payload Generator (24)      |
| `xfreerdp`             | `sudo apt install freerdp2-x11`   | RDP brute force             |
| `aircrack-ng` suite    | `sudo apt install aircrack-ng`    | WiFi Tools (17)             |
| `traceroute`, `whois`  | `sudo apt install traceroute whois` | Network Scanner          |

---

## 🗂️ Modules — v5.0 (40 total)

### Attack & Exploit
| #  | Module |
|----|--------|
| 01 | DDoS Flood — 9 techniques (UDP/SYN/HTTP/Slowloris/POST/RUDY/DNS/ICMP/SSL-reneg) |
| 03 | XSS Injector — 20+ payloads |
| 04 | SQL Injector — error & time based |
| 05 | Brute Force — SSH · FTP · HTTP · WordPress · SMB · MySQL · RDP |
| 25 | ARP Spoofer — MITM Layer 2 |
| 28 | XXE Injection — 7 payloads incl. Billion Laughs |
| 29 | SSRF Scanner — AWS/GCP metadata probes |

### Reconnaissance & Scanning
| #  | Module |
|----|--------|
| 02 | OSINT — email · phone · username · Google dorks |
| 06 | Vulnerability Scanner — headers, SSL, CORS, cookies, .git, methods |
| 07 | Network Scanner — ping sweep, traceroute, whois, geoip, ARP |
| 08 | Port Scanner — 25 ports + banner grab |
| 09 | DNS Enumeration — A/MX/NS/TXT/subdomains |
| 21 | Subdomain Takeover — 13 providers |
| 22 | Shodan Search — query + host info |
| 26 | CVE Scanner — NVD API + auto banner lookup |
| 30 | Packet Sniffer — HTTP creds / DNS / general |
| 32 | TechInt Analyzer — stack fingerprinting |
| 34 | **Public Cameras** — Shodan/Insecam dork generator |
| 36 | **ASN Lookup** — identify network owner |
| 37 | **Wayback Search** — archived URL discovery |
| 38 | **SSL Inspector** — full cert + SAN dump |

### Crypto & Forensics
| #  | Module |
|----|--------|
| 10 | Hash & Encode — MD5/SHA/NTLM + Base64/Hex |
| 11 | Crypto Tools — AES-256, RSA, Caesar brute, HMAC, XOR, auto-decode |
| 19 | Steganography — LSB hide/extract, strings |
| 20 | JWT Tool — decode, none-alg, brute HS256 |
| 23 | File Analyzer + **Virus Scanner** — magic bytes, hashes, entropy, local AV, VirusTotal |
| 31 | Image Metadata — full EXIF + GPS → Google Maps |
| 40 | **Hash Cracker** — offline dict attack MD5/SHA1/SHA256/SHA512 |

### Offensive tooling
| #  | Module |
|----|--------|
| 14 | Web Hacking Suite — directory buster |
| 15 | Phishing Tools — ZPhisher integration |
| 16 | Reverse Shell Generator — 14 langs + TTY upgrade guide |
| 17 | WiFi Tools — aircrack-ng suite |
| 18 | Metasploit Helper — msfvenom cheatsheet |
| 24 | Payload Generator — msfvenom wrapper + XOR / PS base64 |
| 27 | Wordlist Generator — leet-speak + year mutations |

### Intel / OSINT
| #  | Module |
|----|--------|
| 13 | Social Media Tools — 50+ platforms |
| 33 | Phone Lookup — country, carrier, WhatsApp/Telegram probe |
| 35 | **Paste Search** — Pastebin/Ghostbin/IntelX credential leaks |
| 39 | **Breach Check** — HIBP + DeHashed/LeakCheck dorks |

### AI
| #  | Module |
|----|--------|
| 12 | AI Chatbot — **15 models** including uncensored (Dolphin, Hermes, WizardLM) |

---

## 🤖 AI Chatbot (module 12)

**Default: `Dolphin 3.0 Mistral 24B` in DAN (uncensored) mode.**

### Available models (via OpenRouter)

| Tier | Models |
|------|--------|
| **Uncensored** | Dolphin 3.0 Mistral 24B · Dolphin 2.9 Llama 3 · Venice · Hermes 3 405B · WizardLM-2 8x22B |
| **Mainstream** | DeepSeek Chat V3 · DeepSeek R1 · Claude Sonnet 4.5 · Claude Opus 4.1 · GPT-4o · GPT-4o Mini · Gemini 2.0 Flash · Llama 3.3 70B · Qwen 2.5 Coder · Mistral Large |

### Setup

1. Get a free OpenRouter key → [openrouter.ai/keys](https://openrouter.ai/keys)
2. Launch module 12 → paste key on first run
3. Saved to `~/AllInOneTool/tools/.openrouter_key` (chmod 600)

### In-chat commands

| Command    | Action                                                   |
|------------|----------------------------------------------------------|
| `/model`   | Switch model (numbered list)                             |
| `/style`   | Switch style: **uncensored** / hacker / explain / coder / ctf |
| `/clear`   | Reset conversation history                               |
| `/history` | Show conversation so far                                 |
| `/save`    | Save chat to markdown                                    |
| `/exit`    | Back to main menu                                        |

---

## ⚠️ Known Issues

- **Social Media Tools (13)** — several platforms actively block automated requests.
- **WiFi, ARP Spoof, Packet Sniff** — require root + Linux.
- **Phishing (15)** — Linux only, needs `git`.
- **Windows** — a few modules rely on Unix-only commands (`ping -c`, `traceroute`). Use WSL for full compat.

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
| DDoS (all 9 vectors)     | ✅    | ✅      | ✅    | ✅     |
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

**cameleonnbss** — *signed camzzz*

- 🐙 GitHub : [github.com/cameleonnbss](https://github.com/cameleonnbss)

---

## ⚖️ Disclaimer

This toolkit is provided **for educational purposes, authorized penetration testing, and CTF challenges only**. The author is **NOT responsible** for any misuse. Only run it against systems you own or are explicitly authorized to test. **Enjoy your hacking day.**
