

**All-in-one offensive security toolkit**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Termux-brightgreen)
![Language](https://img.shields.io/badge/Also%20in-Rust%20%7C%20C-orange)
![License](https://img.shields.io/badge/Use-Authorized%20Pentest%20%2F%20CTF%20only-red)

</div>

---

## What's inside

| File | Description |
|------|-------------|
| `multi-tool.py` | Main toolkit — 40+ modules, arrow-key UI |
| `rat/builder.py` | Payload builder — generates victim file |
| `rat/c2/server.py` | C2 server — receives loot from victims |
| `rat/rat.rs` | Rust RAT — TCP reverse shell, menu-driven |
| `rat/dropper.c` | C dropper — standalone Windows .exe |
| `requirements.txt` | Python dependencies |
| `requirements-termux.txt` | Termux-compatible subset |
| `install.bat` | One-click installer (Windows) |

---

## Quick start

### Windows
```bat
git clone https://github.com/cameleonnbss/camzzz-multitool
cd camzzz-multitool
install.bat
python multi-tool.py
```

### Linux
```bash
git clone https://github.com/cameleonnbss/camzzz-multitool
cd camzzz-multitool
pip install -r requirements.txt
python3 multi-tool.py
```

### Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install python git clang libffi openssl libjpeg-turbo -y
git clone https://github.com/cameleonnbss/camzzz-multitool
cd camzzz-multitool
pip install -r requirements-termux.txt
python3 multi-tool.py
```

---

## Navigation

The main tool has a **violet arrow-key UI**:

| Key | Action |
|-----|--------|
| `↑` `↓` | Move in column |
| `←` `→` | Switch column |
| `Enter` | Launch module |
| `M` | Text menu (fallback) |
| `Q` | Quit |

---

## Modules

### Attack
| Module | Description |
|--------|-------------|
| **DDoS Flood** | 11 vectors — UDP, SYN, HTTP, Slowloris, POST, ICMP, HULK, R.U.D.Y, SSL. Mode `[E]` ULTRA launches all at max threads |
| Steam Phish | Steam login phishing page |
| Discord Steal | Token + cookie stealer |
| **Discord RAT** | Python bot RAT / Rust TCP RAT / Simple dropper |
| Brute Force | SSH, FTP, RDP, HTTP |
| Payload Gen | Reverse shells, MSFvenom |

### OSINT
| Module | Description |
|--------|-------------|
| **OSINT Pro** | Email, username, domain, Shodan, breaches |
| Phone Lookup | Carrier, country, timezone |
| Pub Cameras | Open RTSP feeds |
| Paste Search | Pastebin / ghostbin |
| ASN Lookup | BGP, IP ranges |
| Wayback | Wayback Machine |

### Web
| Module | Description |
|--------|-------------|
| XSS Injector | 20 payloads, GET + POST |
| SQL Injector | Error-based, boolean |
| Vuln Scanner | XSS, SQLi, IDOR, SSRF, LFI, CMDi, SSTI, headers |
| Web Hacking | Crawler, forms, JS secrets |
| SSRF Scanner | Internal redirect, cloud metadata |
| XXE Inject | XML external entity |

### Network
| Module | Description |
|--------|-------------|
| Port Scanner | TCP connect, service detection |
| DNS Enum | A, MX, NS, TXT, AXFR |
| WiFi Tools | Scanner, deauth, WPS, MAC |
| Packet Sniff | Live capture |
| ARP Spoofer | MITM |
| SSL Inspect | Cert info, expiry |

### Pentest+
| Module | Description |
|--------|-------------|
| Rev Shell | 14 shell types + TTY upgrade |
| Metasploit | Helper one-liners |
| CVE Scanner | CVE lookup by product |
| Wordlist Gen | Custom wordlists |
| Sub Takeover | CNAME takeover check |
| JWT Tool | Decode, forge, alg:none |

### Crypto / Files
| Module | Description |
|--------|-------------|
| Hash+Encode | MD5, SHA, Base64, Caesar |
| Breach Check | HIBP, DeHashed, IntelX |
| Hash Crack | Dictionary + rainbow |
| Steganography | LSB hide/extract PNG |
| File+Virus | Static AV + VirusTotal |
| Image Meta | EXIF extractor |

### Recon / Extra
| Module | Description |
|--------|-------------|
| **AI Chatbot** | OpenRouter — 10 models, Dolphin/Hermes/Nemotron, auto-fallback, DAN mode |
| Shodan | Search + API |
| **File Hider** | Hide any file in any carrier. Change .exe icon. Auto-extract launcher |
| **Social Media** | TikTok info + mass reporter (12 platforms) |
| **Phishing** | Built-in pages: Instagram, Facebook, Google, Discord, TikTok, Microsoft |
| **Geo Photo** | EXIF GPS → coordinates + address + Maps links |

---

## DDoS methods

| Key | Method | Layer |
|-----|--------|-------|
| 1 | UDP Flood | L4 |
| 2 | TCP SYN Flood | L4 |
| 3 | HTTP GET Flood | L7 |
| 4 | Slowloris | L7 |
| 5 | HTTP POST Flood | L7 |
| 6 | R.U.D.Y | L7 |
| 7 | DNS Amplification | L7 |
| 8 | ICMP Flood | L3 |
| 9 | SSL Renegotiation | L7 |
| B | HULK (infinite random GET) | L7 |
| C | GET Flood Auto (timed) | L7 |
| D | POST Flood Auto (timed) | L7 |
| **E** | **ULTRA — all 11 at max threads** | **ALL** |

Port is **auto-detected** from URL (`https://` → 443, `http://` → 80, explicit port kept).

---

## RAT system

See [`rat/README.md`](rat/README.md) for full details.

**3-step workflow:**
1. Run `rat/c2/server.py` on your machine → get URL
2. Run `rat/builder.py` → enter C2 URL → generates payload
3. Victim opens payload → everything lands in `loot/<hostname>/`

**What you receive:**
- `sysinfo.txt` — OS, user, IP, admin status
- `screenshot.png` — screen capture
- `webcam.jpg` — webcam photo
- `keylog.txt` — live keylog updated every 30s
- `wifi.txt` — all wifi passwords
- `files.txt` — Desktop/Downloads/Documents listing
- `loot.zip` — full archive every hour

---

## AI Chatbot

Powered by [OpenRouter](https://openrouter.ai/keys) (free tier).

| Model | Notes |
|-------|-------|
| Gemma 4 26B | Default |
| Dolphin Venice 24B | Zero filter |
| Hermes 3 405B | Low-refusal |
| Nemotron Ultra 253B | NVIDIA |
| Llama 3.3 70B | Meta |

In-chat: `/model` `/style` `/clear` `/history` `/save` `/exit`

---

## Disclaimer

> For **authorized penetration testing, CTF competitions, and educational use only.**
> Do not use against systems you do not own or have explicit written permission to test.
> The author is not responsible for any misuse.

**By camzzz** — [github.com/cameleonnbss](https://github.com/cameleonnbss)
