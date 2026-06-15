<div align="center">

```
            _      _        _____ _   _    ____  _   _ ______ 
     /\   | |    | |      |_   _| \ | |  / __ \| \ | |  ____|
    /  \  | |    | |        | | |  \| | | |  | |  \| | |__   
   / /\ \ | |    | |        | | | . ` | | |  | | . ` |  __|  
  / ____ \| |____| |____   _| |_| |\  | | |__| | |\  | |____ 
 /_/    \_\______|______| |_____|_| \_|  \____/|_| \_|______|
                                                             
                                                             
```

<h3>v5 · by camzzz · 

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20·%20Linux%20·%20Termux-2ea44f?style=flat-square)](.)
[![Languages](https://img.shields.io/badge/Also%20in-Rust%20·%20C-orange?style=flat-square)](.)
[![Use](https://img.shields.io/badge/Use-CTF%20·%20Pentest%20·%20Research-red?style=flat-square)](.)

> **40+ modules** · Arrow-key UI · DDoS engine · RAT system · AI chatbot · Phishing · OSINT · File hider

</div>

---

## Contents

- [Install](#install)
- [Navigation](#navigation)
- [Modules](#modules)
- [DDoS Engine](#ddos-engine)
- [RAT System](#rat-system)
- [AI Chatbot](#ai-chatbot)
- [File Hider](#file-hider)

---

## Install

<details>
<summary><b>Windows</b></summary>

```bat
git clone https://github.com/cameleonnbss/all-in-one-multi-tool
cd all-in-one-multi-tool
install.bat
python multi-tool.py
```
</details>

<details>
<summary><b>Linux / Kali / Parrot</b></summary>

```bash
git clone https://github.com/cameleonnbss/all-in-one-multi-tool
cd all-in-one-multi-tool
pip install -r requirements.txt
python3 multi-tool.py
```
</details>

<details>
<summary><b>Termux (Android)</b></summary>

```bash
pkg update && pkg upgrade -y
pkg install python git clang libffi openssl libjpeg-turbo -y
git clone https://github.com/cameleonnbss/all-in-one-multi-tool
cd all-in-one-multi-tool
pip install -r requirements-termux.txt
python3 multi-tool.py
```
</details>

---

## Navigation

The main UI uses **animated arrow-key navigation** — works on Windows, Linux and Termux.

| Key | Action |
|-----|--------|
| `↑` `↓` | Move up / down |
| `←` `→` | Switch column |
| `Enter` | Launch module |
| `M` | Text menu fallback |
| `Q` | Quit |

---

## Modules

### ⚔️ Attack

| Module | What it does |
|--------|-------------|
| **DDoS Flood** | 11 vectors simultaneously — see [DDoS Engine](#ddos-engine) |
| Steam Phish | Cloned Steam login page |
| Discord Steal | Token + cookie + browser stealer |
| **RAT** | Python / Rust / C — see [RAT System](#rat-system) |
| Brute Force | SSH · FTP · RDP · HTTP |
| Payload Gen | 14 reverse shell types + MSFvenom |

### 🔍 OSINT

| Module | What it does |
|--------|-------------|
| **OSINT Pro** | Email · username · domain · Shodan · breaches · Gravatar |
| Phone Lookup | Carrier · country · timezone · OSINT links |
| Pub Cameras | Open RTSP / MJPEG feeds |
| Paste Search | Pastebin · Ghostbin · Rentry |
| ASN Lookup | BGP · IP ranges · routing |
| Wayback | Archive snapshots |

### 🌐 Web

| Module | What it does |
|--------|-------------|
| XSS Injector | 20 payloads · GET + POST |
| SQL Injector | Error-based · boolean-based |
| **Vuln Scanner** | XSS · SQLi · IDOR · SSRF · LFI · CMDi · SSTI · headers · cookies |
| Web Hacking | Crawler · forms · JS secrets · API endpoints |
| SSRF Scanner | Internal redirect · AWS metadata |
| XXE Inject | XML external entity payloads |

### 📡 Network

| Module | What it does |
|--------|-------------|
| Port Scanner | TCP connect · service detection |
| DNS Enum | A · MX · NS · TXT · AXFR |
| WiFi Tools | Scanner · deauth · WPS · MAC changer |
| Packet Sniff | Live capture |
| ARP Spoofer | MITM poisoning |
| SSL Inspect | Cert · expiry · SAN |

### 🔓 Pentest+

| Module | What it does |
|--------|-------------|
| Rev Shell | 14 shell types + TTY upgrade guide |
| Metasploit | Helper one-liners |
| CVE Scanner | CVE lookup by product |
| Wordlist Gen | Custom wordlists from target info |
| Sub Takeover | CNAME takeover detection |
| JWT Tool | Decode · forge · alg:none |

### 🔐 Crypto / Files

| Module | What it does |
|--------|-------------|
| Hash+Encode | MD5 · SHA1/256/512 · Base64 · Caesar · ROT13 |
| Breach Check | HIBP · DeHashed · IntelX |
| Hash Crack | Dictionary + rainbow table |
| Steganography | LSB hide/extract in PNG |
| File+Virus | Static AV scan + VirusTotal |
| Image Meta | Full EXIF extractor |

### 🛠️ Recon / Extra

| Module | What it does |
|--------|-------------|
| **AI Chatbot** | 10 models · uncensored · auto-fallback — see [AI Chatbot](#ai-chatbot) |
| Shodan | Search + API integration |
| **File Hider** | Hide any file in any carrier — see [File Hider](#file-hider) |
| **Social Media** | TikTok info · mass reporter (12 platforms) · auto HTTP reports |
| **Phishing** | Built-in: Instagram · Facebook · Google · Discord · TikTok · Microsoft |
| **Geo Photo** | EXIF GPS → exact coords + address + Google Maps |

---

## DDoS Engine

Port is **auto-detected** from URL — `https://` → 443, `http://` → 80.

| Key | Method | Layer | Notes |
|-----|--------|-------|-------|
| `1` | UDP Flood | L4 | Raw UDP packets |
| `2` | TCP SYN Flood | L4 | Half-open connections |
| `3` | HTTP GET Flood | L7 | High RPS |
| `4` | Slowloris | L7 | Low bandwidth |
| `5` | HTTP POST Flood | L7 | Heavy body |
| `6` | R.U.D.Y | L7 | 1 byte per 12s |
| `7` | DNS Amplification | L7 | Resolver flood |
| `8` | ICMP Flood | L3 | Ping 1400 bytes |
| `9` | SSL Renegotiation | L7 | CPU exhaustion |
| `B` | HULK | L7 | Random GET, infinite |
| `C` | GET Flood Auto | L7 | Timed + pooled |
| `D` | POST Flood Auto | L7 | Random JSON |
| **`E`** | **ULTRA** | **ALL** | **All 11 vectors at max threads** |

---

## RAT System

Three options — pick the one that fits your target:

| | Simple Dropper | Rust RAT | C Dropper |
|-|----------------|----------|-----------|
| **Platform** | Win + Linux | Win + Linux | Windows only |
| **Size** | 5KB py / 10MB exe | ~200KB | ~80KB |
| **Interactive** | ✗ | ✓ menu-driven | ✗ |
| **Deps on victim** | Python (py) / none (exe) | **Zero** | **Zero** |
| **C2** | HTTP server | netcat | HTTP server |

**Simple Dropper** — victim opens file → you receive in `loot/<hostname>/`:
- `sysinfo.txt` · `screenshot.png` · `webcam.jpg` · `keylog.txt` · `wifi.txt` · `files.txt` · `loot.zip`

**Rust RAT** — menu in your terminal, type numbers:
```
[1] Sysinfo  [2] Screenshot  [3] Webcam  [4] Keylog 30s
[5] Files    [6] Browse dir  [7] Download file  [8] Run cmd
[9] Processes  [10] Kill  [11] Wifi passwords  [12] Browser passwords
[13] Persistence  [14] Free shell  [0] Disconnect
```

**C Dropper** — ~80KB standalone `.exe`, GDI screenshot, wifi, file listing. Compile:
```bash
# Linux → Windows
x86_64-w64-mingw32-gcc dropper.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -mwindows -O2
```

---

## AI Chatbot

Powered by [OpenRouter](https://openrouter.ai/keys) — **free tier**, no payment needed.

| Model | Notes |
|-------|-------|
| Gemma 4 26B | Default |
| **Dolphin Venice 24B** | Zero filter, no refusals |
| **Hermes 3 405B** | Low-refusal, 405B params |
| Nemotron Ultra 253B | NVIDIA |
| Llama 3.3 70B | Meta |

Auto-fallback — if one model fails, tries the next automatically.

In-chat commands: `/model` `/style` `/clear` `/history` `/save` `/exit`

---

## File Hider

Hide any file (`.exe`, `.py`, `.sh`, `.zip`...) inside any carrier (image, PDF, MP4...).

| Option | Description |
|--------|-------------|
| **Hide** | Embed payload inside carrier |
| **Extract** | Recover hidden payload |
| **Scan** | Detect if a file has a hidden payload |
| **Icon** | Change `.exe` icon from `.png`/`.ico` (Windows) |
| **Launcher** | Generate `.py` that auto-extracts and runs |

---

## Disclaimer

> For **authorized penetration testing, CTF competitions, and educational use only.**  
> Do not use against systems you do not own or have explicit written permission to test.  
> The author is not responsible for any misuse.

**By camzzz** — [github.com/cameleonnbss](https://github.com/cameleonnbss)
**discord** : cameleonmortis_new
<div align="center">

