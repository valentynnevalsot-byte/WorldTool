#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WORLDtooL - created by injectorX69 - cyber security framework

import os
import sys
import time
import shutil
import socket
import subprocess
import urllib.request

# ---------------- ASCII LOGO: WORLDtooL (velke a hezke) ----------------
LOGO = r"""
██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ ████████╗ ██████╗  ██████╗ ██╗
██║    ██║██╔═══██╗██╔══██╗██║    ██╔═══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║
██║ █╗ ██║██║   ██║██████╔╝██║    ██║   ██║   ██║   ██║   ██║██║   ██║██║
██║███╗██║██║   ██║██╔══██╗██║    ██║   ██║   ██║   ██║   ██║██║   ██║██║
╚███╔███╔╝╚██████╔╝██║  ██║███████╗╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝██║
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═╝
      t o o L  ~  created by injectorX69  ~  cyber security framework
"""

# ---------------- HELPERS ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def term_size():
    return shutil.get_terminal_size((100, 30))

def center(text):
    cols, _ = term_size()
    return "\n".join(l[:cols].center(cols) if l.strip() else "" for l in text.split("\n"))

def valid_ip(host):
    try:
        socket.inet_aton(host)
        return True
    except (socket.error, OSError):
        return False

def resolve(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

# ---------------- 1) LOADING BAR ----------------
def loading_bar():
    clear()
    print("\n\n" + center(LOGO))
    print(center("Loading WORLDtooL...\n"))
    bar_len = 50
    for i in range(bar_len + 1):
        pct = int(100 * i / bar_len)
        bar = "#" * i + "-" * (bar_len - i)
        print(f"\r   [{bar}] {pct:3d}%", end="", flush=True)
        time.sleep(0.03)
    print()

# ---------------- 2) SHIMMER (bila vlna prejizdi pres logo) ----------------
def shimmer_logo():
    lines = LOGO.split("\n")
    print("\033[?25l", end="")
    try:
        for frame in range(50):
            wave = frame % (len(lines) + 8) - 4
            clear()
            print("\n")
            for i, line in enumerate(lines):
                dist = abs(i - wave)
                if dist == 0:
                    print("\033[1;97m\033[5m" + line + "\033[0m")  # bila blikajici vlna
                elif dist == 1:
                    print("\033[1;97m" + line + "\033[0m")
                elif dist == 2:
                    print("\033[1;37m" + line + "\033[0m")
                elif dist == 3:
                    print("\033[1;90m" + line + "\033[0m")
                else:
                    print("\033[0;90m" + line + "\033[0m")
            time.sleep(0.07)
    finally:
        print("\033[?25h", end="")

# ---------------- 3) SPINNER LOADING ----------------
def spinner_loading():
    spin = itertools.cycle(["|", "/", "-", "\\"])
    print("\033[?25l", end="")
    try:
        for _ in range(30):
            clear()
            print("\n" + center(LOGO))
            print(center(f"\n   Loading modules... {next(spin)}"))
            time.sleep(0.1)
    finally:
        print("\033[?25h", end="")

# ================= FUNKCNI NASTROJE =================

# 1. Reconnaissance
def tool_recon():
    host = input("\n   [?] Target (domain or IP): ").strip()
    ip = host if valid_ip(host) else resolve(host)
    if not ip:
        print("   [!] Could not resolve host.")
        return
    print(f"\n   [+] IP address: {ip}")
    try:
        socket.setdefaulttimeout(3)
        hostname, _, _ = socket.gethostbyaddr(ip)
        print(f"   [+] Reverse DNS: {hostname}")
    except Exception:
        print("   [-] Reverse DNS: not found")
    for port in (21, 22, 80, 443, 3389):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        if s.connect_ex((ip, port)) == 0:
            print(f"   [+] Port {port}: OPEN")
        s.close()

# 2. nmap
def tool_nmap():
    target = input("\n   [?] Target IP: ").strip()
    args = input("   [?] nmap args (enter = -sV): ").strip() or "-sV"
    if not shutil.which("nmap"):
        print("   [!] nmap is not installed. (apt install nmap)")
        return
    subprocess.call(["nmap", *args.split(), target])

# 3. IP lookup
def tool_iplookup():
    host = input("\n   [?] Domain or IP: ").strip()
    ip = host if valid_ip(host) else resolve(host)
    if not ip:
        print("   [!] Could not resolve.")
        return
    print(f"   [+] Resolved IP: {ip}")
    try:
        with urllib.request.urlopen(f"https://ipinfo.io/{ip}/json", timeout=8) as r:
            print(r.read().decode())
    except Exception as e:
        print(f"   [!] Lookup failed: {e}")

# 9. DNS lookup
def tool_dns():
    import socket as s
    host = input("\n   [?] Domain: ").strip()
    for rtype in ("A", "AAAA", "MX", "NS"):
        try:
            ans = s.getaddrinfo(host, None)
            ips = sorted({a[4][0] for a in ans})
            print(f"   [+] {rtype}: {', '.join(ips)}")
            break
        except Exception:
            pass
    try:
        with urllib.request.urlopen(f"https://dns.google/resolve?name={host}&type=MX", timeout=8) as r:
            print(r.read().decode())
    except Exception as e:
        print(f"   [!] MX lookup failed: {e}")

# 10. Ip changer
def tool_ipchanger():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=8) as r:
            print(f"\n   [+] Your public IP: {r.read().decode()}")
    except Exception as e:
        print(f"   [!] Failed: {e}")
    if os.name == "nt":
        print("   [i] Windows: ipconfig /release && ipconfig /renew")
    else:
        print("   [i] Linux: restart dhclient or reconnect network.")

# 11. AdminFinder/WEB
ADMIN_PATHS = ["admin", "admin/login.php", "adminpanel", "administrator",
               "login", "panel", "dashboard", "admin/admin.php", "manager", "cp"]

def tool_adminfinder():
    url = input("\n   [?] Target URL (http://target): ").strip().rstrip("/")
    if not url.startswith("http"):
        url = "http://" + url
    print("   [*] Scanning...")
    for p in ADMIN_PATHS:
        try:
            with urllib.request.urlopen(f"{url}/{p}", timeout=5) as r:
                if r.status == 200:
                    print(f"   [+] FOUND: {url}/{p} (200 OK)")
        except Exception:
            pass
    print("   [*] Done.")

# 12. MAC ADDRESS Lookup
def tool_maclookup():
    if os.name == "nt":
        os.system("getmac /v")
    else:
        os.system("ip link show")

# 24. SQLmap
def tool_sqlmap():
    url = input("\n   [?] Target URL: ").strip()
    if not shutil.which("sqlmap"):
        print("   [!] sqlmap is not installed. (apt install sqlmap)")
        return
    subprocess.call(["sqlmap", "-u", url, "--batch"])

FUNCTIONAL = {
    1:  ("Reconnaissance",     tool_recon),
    2:  ("nmap",               tool_nmap),
    3:  ("IP lookup",          tool_iplookup),
    9:  ("DNS lookup",         tool_dns),
    10: ("Ip changer",         tool_ipchanger),
    11: ("AdminFinder/WEB",    tool_adminfinder),
    12: ("mac ADRESS Lookup",  tool_maclookup),
    24: ("SQLmap",             tool_sqlmap),
}

# ---------------- MENU ----------------
TOOLS = [
    "Reconnaissance", "nmap", "IP lookup", "DDoS", "DOS", "Wifi.Pass", "WIFIdos",
    "PhoneNumberTRac", "Spoof", "DNS lookup", "Ip changer", "AdminFinder/WEB",
    "mac ADRESS Lookup", "Tiktok OSINT", "INSTAGRMA OSNT", "DISCORD OSINT",
    "Virus creator", "Tv.hack", "wifiKilller", "WhatsOSINT", "OSINT",
    "Tl luncher osint", "Map finder", "SQLmap", "Injectweb", "COMMIX",
    "Phisngsite", "Loaclhost web creator", "find teh all inf", "RAT",
]

def menu():
    while True:
        clear()
        print("\033[1;97m" + center(LOGO) + "\033[0m")
        print(center("=== WORLDtooL Framework | created by injectorX69 ===\n"))
        for i, t in enumerate(TOOLS, 1):
            mark = " [OK]" if i in FUNCTIONAL else ""
            print(f"   {i:2d}. {t}{mark}")
        print("    0. exit")
        choice = input("\n   Select tool: ").strip()
        if choice in ("0", "exit", "quit"):
            clear()
            print(center("\n\n  Exiting WORLDtooL... stay secure!\n"))
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(TOOLS):
            idx = int(choice)
            name = TOOLS[idx - 1]
            if idx in FUNCTIONAL:
                try:
                    FUNCTIONAL[idx][1]()
                except KeyboardInterrupt:
                    print("\n   [!] Cancelled.")
            else:
                print(f"\n   [i] Module '{name}' is not implemented yet - placeholder.")
            input("   Press Enter to continue...")
        else:
            print("   [!] Invalid choice!")
            time.sleep(1)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    import itertools
    try:
        loading_bar()
        shimmer_logo()
        spinner_loading()
        menu()
    except KeyboardInterrupt:
        clear()
        print("\n  [!] Interrupted - exiting WORLDtooL.\n")
        sys.exit(0)
