# 🛠️ ALL IN ONE TOOL v5

> All-In-One Hacking Toolkit — 40+ modules, UI violet animée, modules inline, AI chatbot avec fallback automatique.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Termux-lightgrey)
![Modules](https://img.shields.io/badge/Modules-40%2B-green)
![AI](https://img.shields.io/badge/AI-Uncensored-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-Educational%20Only-red)

---

## ⚡ Quick Start

### Windows — Setup automatique
```bat
setup.bat
```

### Manuel (tous OS)
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python multi-tooV5-fixed.py
```

---

## 🚀 Installation par OS

### 🐧 Linux (Ubuntu / Debian / Kali)
```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip3 install -r requirements.txt --break-system-packages
python3 multi-toolV5.py
```

### 🍎 macOS
```bash
brew install git python
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 multi-toolV5.py
```

### 🪟 Windows
Double-clique sur `setup.bat` — installe tout et lance le tool.

Ou manuellement :
```powershell
pip install -r requirements.txt
python multi-toolV5.py
```

### 📱 Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/cameleonnbss/all-in-one-multi-tool.git
cd all-in-one-multi-tool
pip install -r requirements.txt
python multi-toolV5.py
```

> Les modules 17 (WiFi), 25 (ARP), 30 (Packet Sniff) nécessitent root sur Termux.

---

## 🗂️ Modules — v5 (40+)

### ⚔️ Attack
| # | Module | Description |
|---|--------|-------------|
| 01 | DDoS Flood | 9 techniques : UDP · SYN · HTTP · Slowloris · POST · RUDY · DNS · ICMP · SSL |
| 03 | XSS Injector | 20+ payloads GET/POST |
| 04 | SQL Injector | Error-based + time-based |
| 05 | Brute Force | SSH · FTP · HTTP · WordPress · SMB · MySQL · RDP |
| 25 | ARP Spoofer | MITM Layer 2 |
| 28 | XXE Injection | 7 payloads dont Billion Laughs |
| 29 | SSRF Scanner | AWS/GCP metadata probes |
| St | Steam Phishing | Page login Steam via ngrok (inline) |
| DS | Discord Stealer | Cookies Firefox/Chrome + tokens Discord → webhook (inline) |
| DR | Discord RAT | Bot C2 via Discord — !cmd !webcam !keylogger... (inline) |

### 🔍 OSINT & Recon
| # | Module | Description |
|---|--------|-------------|
| 02 | OSINT Pro | Email · phone · username · Google dorks |
| 06 | Vuln Scanner | Headers, SSL, CORS, cookies, .git |
| 07 | Network Scanner | Ping sweep, traceroute, whois, geoip |
| 08 | Port Scanner | 25 ports + banner grab |
| 09 | DNS Enum | A/MX/NS/TXT/subdomains |
| 21 | Sub Takeover | 13 providers |
| 22 | Shodan | Query + host info |
| 26 | CVE Scanner | NVD API + banner |
| 30 | Packet Sniff | HTTP creds / DNS |
| 32 | TechInt | Stack fingerprinting |
| 33 | Phone Lookup | Carrier · timezone · OSINT links |
| 34 | Pub Cameras | Shodan/Insecam dorks |
| 36 | ASN Lookup | Network owner |
| 37 | Wayback | URL archive discovery |
| 38 | SSL Inspector | Cert + SAN dump |

### 🔐 Crypto & Forensics
| # | Module |
|---|--------|
| 10 | Hash & Encode — MD5/SHA/NTLM + Base64/Hex |
| 11 | Crypto Tools — AES-256, RSA, Caesar brute, HMAC, XOR |
| 19 | Steganography — LSB hide/extract |
| 20 | JWT Tool — decode, none-alg, brute HS256 |
| 23 | File + Virus Scanner — magic bytes, hashes, entropy, VirusTotal |
| 31 | Image Meta — EXIF + GPS → Google Maps |
| 40 | Hash Cracker — dict attack MD5/SHA1/SHA256 |

### 💣 Offensive
| # | Module |
|---|--------|
| 14 | Web Hacking Suite — directory buster |
| 15 | Phishing Tools |
| 16 | Rev Shell — 14 langages |
| 17 | WiFi Tools — aircrack-ng suite |
| 18 | Metasploit Helper — cheatsheet msfvenom |
| 24 | Payload Gen — msfvenom wrapper + XOR/PS |
| 27 | Wordlist Gen — leet + mutations |

### 🤖 AI & Extra
| # | Module |
|---|--------|
| 12 | AI Chatbot — fallback automatique sur 10 modèles |
| 13 | Social Media — 50+ plateformes |
| 35 | Paste Search — Pastebin/Ghostbin/IntelX |
| 39 | Breach Check — HIBP + leaks |

---

## 🤖 AI Chatbot (module 12)

Fallback automatique : si un modèle est en 429/404, passe au suivant jusqu'à obtenir une réponse.

**Modèles disponibles :**

| Statut | Modèle |
|--------|--------|
| ✅ Actif | Gemma 4 26B · Gemma 4 31B · Nemotron 120B · GPT-OSS 120B |
| 🔄 Selon quota | Dolphin Venice 24B · Hermes 3 405B · Llama 3.3 70B · Qwen3 Coder |

**Setup :** clé OpenRouter gratuite → [openrouter.ai/keys](https://openrouter.ai/keys)

**Commandes in-chat :**
```
/model    changer de modèle
/style    uncensored / hacker / coder / ctf / explain
/clear    reset historique
/history  voir la conversation
/save     sauvegarder en markdown
/exit     retour au menu
```

---

## 📦 Dépendances

```
requests  colorama  beautifulsoup4  dnspython  phonenumbers
cryptography  Pillow  scapy  paramiko  pymysql  impacket
flask  pyngrok
```

Optionnel (Discord RAT) : `discord.py  keyboard  pyautogui  opencv-python  pywin32`

### Outils système (non-pip)

| Outil | Install | Module |
|-------|---------|--------|
| `aircrack-ng` | `sudo apt install aircrack-ng` | 17 WiFi |
| `msfvenom` | Metasploit Framework | 18, 24 |
| `traceroute/whois` | `sudo apt install traceroute whois` | 07 |

---

## 🖥️ Compatibilité

| Module | Linux | Windows | macOS | Termux |
|--------|:-----:|:-------:|:-----:|:------:|
| Core (tous) | ✅ | ✅ | ✅ | ✅ |
| DDoS (9 vecteurs) | ✅ | ✅ | ✅ | ✅ |
| WiFi / ARP / Sniff | ✅ | ❌ | ⚠️ | root |
| Discord RAT | ✅ | ✅ | ✅ | ✅ |
| Steam Phishing | ✅ | ✅ | ✅ | ✅ |
| AI Chatbot | ✅ | ✅ | ✅ | ✅ |
| Port / Net Scanner | ✅ | ✅ | ✅ | ✅ |

---

## ⚠️ Disclaimer

**Usage éducatif, pentest autorisé et CTF uniquement.**  
L'auteur n'est **pas responsable** de toute utilisation abusive.  
Teste uniquement sur des systèmes que tu possèdes ou pour lesquels tu as une autorisation écrite.

---

## 👤 Auteur

**cameleonnbss** — *signed camzzz*  
🐙 [github.com/cameleonnbss](https://github.com/cameleonnbss)

