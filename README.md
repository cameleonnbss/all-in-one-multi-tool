
# 🛠️ CAMZZZ MULTI-TOOL · v3.0

> All-In-One Hacking Toolkit — 13 categories, 50+ tools, one menu.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/License-Educational-red)

---

## ⚡ Quick Start

```bash
git clone https://github.com/youruser/camzzz-multitool.git
cd camzzz-multitool
pip install -r requirements.txt
python3 main.py
```

> Missing `requests` or `colorama`? The script auto-installs them on first run.

---

## 📦 Requirements

| Package    | Purpose              |
|------------|----------------------|
| `requests` | HTTP requests / APIs |
| `colorama` | Terminal colors      |

### System Tools (optional, used by specific modules)

| Tool           | Used By                     |
|----------------|------------------------------|
| `git`          | Auto-cloning tool repos      |
| `hydra`        | SSH / FTP / RDP bruteforce   |
| `fcrackzip`    | Zip file cracking            |
| `pdfcrack`     | PDF file cracking            |
| `nmap`         | Network / port scanning      |
| `sqlmap`       | SQL injection testing        |
| `gobuster`     | Directory brute-forcing      |
| `nikto`        | Web server scanning          |
| `aircrack-ng`  | WiFi handshake / deauth      |
| `reaver`       | WPS pin attacks              |
| `whois`        | Domain registration lookup   |
| `traceroute`   | Network path tracing         |

---

## 🗂️ Modules

### 1 · Bruteforce
Instagram · SSH · FTP · RDP · Zip Cracker · PDF Cracker

### 2 · OSINT
Sherlock · Phone OSINT · Email OSINT / Breach Check · IP Geolocation · Subdomain Finder · Breach Database · Maigret

### 3 · Phishing
ZPhisher · CamPhish · HiddenEye · ShellPhish

### 4 · DDoS
Layer 4 Flood · Slowloris · HULK DoS · DDoS-Ripper · LOIC Clone

### 5 · WiFi Hacking
WiFi Scanner · Handshake Capture · Deauth Attack · WPS Pin Attack · MAC Changer

### 6 · Web Hacking
Nmap Scanner · SQLmap · Gobuster · Nikto · XSStrike (XSS)

### 7 · Social Media
Instagram Report · TikTok Report · Snapchat Report · Facebook Report

### 8 · AI Chatbot
OpenRouter-powered chatbot (DeepSeek model) with local API key storage and offline demo mode.

### 9 · Network Tools
Ping Sweep · DNS Lookup · Traceroute · Reverse DNS · HTTP Header Grab · Port Scanner

### 10 · Crypto Utilities
Hash Generator (MD5 / SHA1 / SHA256) · Base64 Encode/Decode · Password Generator · Caesar Cipher · Hash Identifier

### 11 · Utilities
FSociety Banner · System Info · Public IP · Whois Lookup · Single Port Check

### 12 · Download All Tools
Batch-clones all Git-based tool repos into a local `tools/` directory.

### 13 · Illegal Tools (Simulated)
Ransomware · Keylogger · Botnet — **disabled stubs for educational reference only.**

---

## 🔑 API Keys

| Service      | Where to Get                          | Storage                     |
|--------------|---------------------------------------|-----------------------------|
| OpenRouter   | [openrouter.ai](https://openrouter.ai) | `tools/.openrouter_key`     |

The chatbot prompts for a key on first use and saves it locally.

---

## 📁 Directory Structure

```
camzzz-multitool/
├── main.py               # Entry point
├── requirements.txt
├── README.md
└── tools/                # Auto-created; holds cloned repos
    ├── sherlock/
    ├── zphisher/
    ├── xsstrike/
    └── ...
```

---

## 🖥️ Platform Notes

| Feature              | Linux | Windows |
|----------------------|:-----:|:-------:|
| Core menu & utils    | ✅    | ✅      |
| WiFi modules         | ✅    | ⚠️ Limited |
| Hydra / aircrack-ng  | ✅    | ❌ Requires WSL |
| Ping sweep           | ✅    | ✅      |
| Whois                | ✅    | 🌐 Web fallback |

---

## ⚠️ Disclaimer

This toolkit is provided **for educational and authorized testing purposes only.** Unauthorized use against systems you do not own or have explicit permission to test is illegal. The author assumes no liability for misuse.

---

## 👤 Author

**camzzz**

---
```

Both files are ready to drop straight into your repo root. Let me know if you want the README tweaked to V7 branding instead, or if you've got updated module lists to fold in.
