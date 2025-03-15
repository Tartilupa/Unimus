import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
import socket
from urllib.parse import urljoin
import os
import sys

# Clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# ASCII Art
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

# WebTree functions
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

def print_tree(tree, indent=0):
    for key, values in tree.items():
        print(" " * indent + "📂 " + key)
        if isinstance(values, dict):
            print_tree(values, indent + 4)

def freeze_web(url):
    print(f"📥 Saving page: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"✅ Page saved as {filename}")
    except requests.RequestException:
        print(Fore.RED + "❌ Error saving page!" + Style.RESET_ALL)

def package_webtree():
    while True:
        try:
            webtree_choice = input("root@localhost/webtree/:~$ ").strip()
            if webtree_choice.startswith("scan "):
                url = webtree_choice.split("scan ")[1]
                print(f"🔍 Scanning links on: {url}")
                tree = get_links(url, url, depth=2)
                print_tree(tree)
            elif webtree_choice.startswith("freeze "):
                url = webtree_choice.split("freeze ")[1]
                freeze_web(url)
            elif webtree_choice.lower() in ["exit", "quit"]:
                break
            elif webtree_choice.lower() == "help":
                print("Available commands:\n scan <url> - Scan a website for links\n freeze <url> - Save a webpage\n exit - Quit package")
            else:
                print(Fore.RED + "Unknown command!" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print("\n⏹️ Interrupt not allowed. Use 'exit' to quit.")

def package_freezeweb():
    while True:
        try:
            freezeweb_choice = input("root@localhost/freezeweb/:~$ ").strip()
            if freezeweb_choice.startswith("freeze "):
                url = freezeweb_choice.split("freeze ")[1]
                freeze_web(url)
            elif freezeweb_choice.lower() in ["exit", "quit"]:
                break
            elif freezeweb_choice.lower() == "help":
                print("Available commands:\n freeze <url> - Save a webpage\n exit - Quit package")
            else:
                print(Fore.RED + "Unknown command!" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print("\n⏹️ Interrupt not allowed. Use 'exit' to quit.")

def main():
    print_banner()
    
    while True:
        try:
            choice_main = input("root@localhost:~$ ").strip()
            
            if choice_main == "package webtree":
                package_webtree()
            elif choice_main == "package freezeweb":
                package_freezeweb()
            elif choice_main.lower() in ["exit", "quit"]:
                print("Exiting program...")
                break
            elif choice_main.lower() == "help":
                print("Available packages:\n package webtree - Scan websites for links\n package freezeweb - Save webpages\n exit - Quit program")
            else:
                print(Fore.RED + "Unknown command!" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print("\n⏹️ Interrupt not allowed. Use 'exit' to quit.")

if __name__ == "__main__":
    main()
