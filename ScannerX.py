import nmap
import socket
import whois
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import tldextract
from colorama import Fore, Style
from pyfiglet import figlet_format
import dns.resolver
from concurrent.futures import ThreadPoolExecutor


# Definizione dei codici di colore ANSI
GREEN = "\033[92m"
RESET = "\033[0m"
RED = "\033[91m"
ORANGE = "\033[93m"

banner_text = figlet_format("ScannerX", font="slant")
print(f"{ORANGE}{banner_text}{RESET}")
print(f"{ORANGE}Written in Python 3.11.6")
print("")
print(f"{ORANGE}by: Konigstiger18")
print("")
print("")
print("")
input(f"{ORANGE}Press Enter to continue...")

def format_dates(dates):
    if isinstance(dates, list):
        return "\n".join(date.strftime("%Y-%m-%d %H:%M:%S") for date in dates)
    else:
        return dates.strftime("%Y-%m-%d %H:%M:%S") if dates else "N/A"

def format_list(items):
    return "\n".join(items) if items else "N/A"

def activate_protonvpn():
    try:
        print("Activating ProtonVPN...")
        # Sostituisci 'your_username' e 'your_password' con le tue credenziali ProtonVPN
        protonvpn_command = f"sudo protonvpn connect"
        subprocess.run(protonvpn_command, shell=True, check=True)
        print("ProtonVPN activated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error activating ProtonVPN: {e}{RESET}")

def deactivate_protonvpn():
    try:
        print("Deactivating ProtonVPN...")
        subprocess.run("sudo protonvpn disconnect", shell=True, check=True)
        print("ProtonVPN deactivated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error deactivating ProtonVPN: {e}{RESET}")

def ask_activate_protonvpn():
    while True:
        user_input = input(f"{ORANGE}Do you want to activate ProtonVPN before proceeding? (y/n): ").lower()
        if user_input == 'y':
            activate_protonvpn()
            return True
        elif user_input == 'n':
            return False
        else:
            print(f"{RED}Invalid input. Please enter 'y' or 'n'.{RESET}")

def scan_ports_with_nmap(target):
    print(f"{ORANGE}Scanning ports:{RESET}\n")
    try:
        # Componi il comando per eseguire la scansione di Nmap
        nmap_command = f"nmap -T3 -p 1-1000 {target}"

        # Esegui il comando e stampa direttamente l'output
        subprocess.call(nmap_command, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"{RED}Nmap scan failed: {e}{RESET}")


def get_abuse_email_registrar(whois_info):
    # Possibili parole chiave associate all'abuso
    abuse_keywords = ["abuse", "report_abuse", "contact", "abuse_contact"]

    # Scansiona tutte le chiavi e i valori alla ricerca di parole chiave associate all'abuso
    for key, value in whois_info.items():
        # Controlla sia la chiave che il valore
        key_lower = key.lower()
        value_lower = str(value).lower()

        for keyword in abuse_keywords:
            if keyword in key_lower or keyword in value_lower:
                return value

    return "N/A"  # Se nessuna corrispondenza viene trovata

def get_whois_info(target):
    try:
        # Ottieni l'indirizzo IP del sito web
        ip_address_site = socket.gethostbyname(target)

        # Verifica se il sito utilizza Cloudflare
        is_cloudflare = check_cloudflare(target)

        w = whois.whois(target)
        print(f"{ORANGE}IP Address:{RESET}\n{ip_address_site}")
        print(f"{ORANGE}Hosting Location:{RESET} {get_hosting_location(target)}")
        print(f"{ORANGE}Registrar:{RESET}\n{w.registrar}")
        print(f"{ORANGE}Registrar Abuse Email:{RESET}\n{get_abuse_email_registrar(w)}")
        print(f"{ORANGE}Registrant Email:{RESET}\n{w.get('email', 'N/A')}")
        print(f"{ORANGE}Creation Date:{RESET}\n{format_dates(w.creation_date)}")
        print(f"{ORANGE}Expiration Date:{RESET}\n{format_dates(w.expiration_date)}")
        print(f"{ORANGE}Cloudflare:{RESET} {'Yes' if is_cloudflare else 'No'}")
        print(f"{ORANGE}Name Servers:{RESET}\n{format_list(w.name_servers)}")
        print(f"{ORANGE}Status:{RESET}\n{', '.join(w.status)}")  # Unisci gli stati in una stringa separata da virgole

    except whois.parser.PywhoisError as e:
        print(f"{RED}Error retrieving Whois information: {e}{RESET}")
    except (socket.error, socket.herror, socket.gaierror) as e:
        print(f"{RED}Error retrieving additional information: {e}{RESET}")

def check_cloudflare(target):
    try:
        # Esegui una richiesta HTTP e verifica le intestazioni della risposta
        response = requests.get(f'http://{target}', timeout=5)
        return 'cloudflare' in response.headers.get('server', '').lower()

    except requests.RequestException:
        return False

def get_hosting_location(domain):
    try:
        # Ottieni l'indirizzo IP del dominio
        ip_address = socket.gethostbyname(domain)

        # Ottieni informazioni sulla geolocalizzazione usando un servizio di geolocalizzazione basato su IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()

        if data['status'] == 'fail':
            print("Failed to retrieve hosting location information.")
            return 'N/A'

        city = data.get('city', 'N/A')
        region = data.get('regionName', 'N/A')
        country = data.get('country', 'N/A')

        return f"{city}, {region}, {country}"

    except socket.gaierror as e:
        print(f"Error resolving domain: {e}")
        return 'N/A'
    except requests.RequestException as e:
        print(f"Error retrieving hosting location information: {e}")
        return 'N/A'

def dns_query_with_metasploit(target_domain, query_types):
    try:
        for query_type in query_types:
            print(f"\nRunning DNS query for {query_type} on {target_domain} using Metasploit...")

            # Componi il comando per eseguire la query DNS con Metasploit
            metasploit_command = f"msfconsole -q -x 'use auxiliary/scanner/dns/dns_amp;set QUERYTYPE {query_type};set RHOSTS {target_domain};run;exit'"

            # Esegui il comando e cattura l'output
            result = subprocess.run(metasploit_command, shell=True, capture_output=True, text=True)

            # Stampa l'output dell'operazione
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running Metasploit DNS query: {e}{RESET}")

def run_nikto_scan(target):
    try:
        print(f"{ORANGE}Running Nikto scan on {target}...{RESET}")
        # Componi il comando per eseguire la scansione Nikto
        nikto_command = f"nikto -h {target}"

        # Esegui il comando e stampa direttamente l'output
        subprocess.call(nikto_command, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running Nikto scan: {e}{RESET}")

def run_sqlmap_scan(target):
    try:
        print(f"{ORANGE}Running SQLmap scan on {target}...{RESET}")
        # Componi il comando per eseguire la scansione SQLmap
        sqlmap_command = f"sqlmap -u {target}"

        # Esegui il comando e stampa direttamente l'output
        subprocess.call(sqlmap_command, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running SQLmap scan: {e}{RESET}")

def get_resource_content(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Funzione per stampare il titolo con stile
def print_title(title):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{title}{Style.RESET_ALL}")

# Funzione per eseguire l'analisi del dominio target
def analyze_target_domain_info(target_domain_url):
    try:
        # Ottieni il contenuto della pagina web
        page_content = get_resource_content(target_domain_url)
        if page_content is None:
            return

        # Creazione del parser HTML
        soup = BeautifulSoup(page_content, 'html.parser')

        # Analizza e stampa le informazioni
        print_title(f"Login pages for {target_domain_url}")
        login_pages = find_login_pages(soup, target_domain_url)
        print(login_pages)

        print_title(f"Robots.txt content for {target_domain_url}")
        robots_txt_url = find_robots_txt_url(target_domain_url)
        robots_txt_content = get_robots_txt_content(robots_txt_url) if robots_txt_url else "File robots.txt not found"
        print(robots_txt_content)

        print_title(f"Subdomains for {target_domain_url}")
        subdomains = find_subdomains(tldextract.extract(target_domain_url).domain)
        print(subdomains)

        print_title("Random Query:")
        random_query = generate_random_query()
        print(random_query)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def print_title(title):
    print(f"{ORANGE}{title}{RESET}")

def find_login_pages(soup, base_url):
    login_pages = []
    try:
        login_forms = soup.find_all('form')
        for form in login_forms:
            action = form.get('action')
            if action and 'login' in action.lower():
                login_pages.append(urljoin(base_url, action))
    except Exception as e:
        raise RuntimeError(f"Error finding login pages: {e}")
    return login_pages

def find_robots_txt_url(url):
    try:
        ext = tldextract.extract(url)
        return f"http://{ext.domain}.{ext.suffix}/robots.txt"
    except Exception as e:
        raise RuntimeError(f"Error building robots.txt URL: {e}")

def get_robots_txt_content(robots_txt_url):
    try:
        response = requests.get(robots_txt_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching robots.txt content: {e}")

def find_subdomains(domain):
    try:
        response = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
        response.raise_for_status()
        data = response.json()
        return [entry.get("name_value", "").strip() for entry in data]
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching subdomains: {e}")

def generate_random_query():
    parameters = ["param1", "param2", "id", "q", "search", "category"]
    values = ["value1", "value2", "123", "query", "keyword", "cat1", "cat2"]
    query = f"{random.choice(parameters)}={random.choice(values)}"
    return query

def main():
    try:
        target_domain_url = input("Enter the target domain: ").strip()

        if not target_domain_url.startswith(("http://", "https://")):
            target_domain_url = "http://" + target_domain_url

        response = requests.get(target_domain_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        print_title(f"Login pages for {target_domain_url}")
        login_pages = find_login_pages(soup, target_domain_url)
        print(login_pages)

        print_title(f"Robots.txt content for {target_domain_url}")
        robots_txt_url = find_robots_txt_url(target_domain_url)
        robots_txt_content = get_robots_txt_content(robots_txt_url) if robots_txt_url else "File robots.txt not found"
        print(robots_txt_content)

        print_title(f"Subdomains for {target_domain_url}")
        subdomains = find_subdomains(tldextract.extract(target_domain_url).domain)
        print(subdomains)

    except requests.RequestException as e:
        print(f"Error fetching {target_domain_url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
# Funzione per generare una query casuale
def generate_random_query():
    parameters = ["param1", "param2", "id", "q", "search", "category"]
    values = ["value1", "value2", "123", "query", "keyword", "cat1", "cat2"]
    query = f"{random.choice(parameters)}={random.choice(values)}"
    return query

def cerca_dominio(nome_dominio):
    estensioni = [
        # Generiche
        ".com", ".net", ".org", ".gov", ".edu", ".biz", ".info", ".name", ".pro", ".mobi", ".int", ".coop", ".aero", ".travel",

        # Nazionali
        ".it", ".fr", ".es", ".de", ".uk", ".us", ".ca", ".au", ".jp", ".cn", ".br", ".ru",
        ".in", ".mx", ".nl", ".nz", ".se", ".ch", ".za", ".ae", ".sa", ".ar", ".id", ".tr",

        # Tech
        ".io", ".ai", ".app", ".dev", ".tech", ".systems", ".web", ".software", ".code", ".data", ".network", ".cloud",

        # Contenuto
        ".blog", ".news", ".info", ".media", ".tv", ".movie", ".music", ".gaming", ".art", ".photo", ".gallery", ".studio",

        # Commercio
        ".store", ".shop", ".market", ".online", ".sale", ".buy", ".discount", ".shop", ".fashion", ".jewelry", ".food", ".restaurant",

        # Professionali
        ".guru", ".expert", ".consulting", ".lawyer", ".doctor", ".engineer", ".architect", ".accountant",
        ".dentist", ".realty", ".consultant", ".coach", ".therapy", ".training", ".education", ".academy",

        # Altre
        ".co", ".me", ".xyz", ".space", ".club", ".live", ".link", ".social", ".design", ".events", ".travel", ".party", ".golf",
        ".fitness", ".photography", ".blog", ".gaming", ".family", ".pet", ".science", ".green", ".eco",
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(verifica_dominio, f"{nome_dominio}{estensione}") for estensione in estensioni]

    for future in futures:
        future.result()

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(verifica_dominio, f"{nome_dominio}{estensione}") for estensione in estensioni]

    for future in futures:
        future.result()
        
def verifica_dominio(dominio):
    try:
        answers = dns.resolver.resolve(dominio, 'A')
        print(f"The domain {dominio} is {Fore.GREEN}registered{Fore.RESET}.")
    except dns.resolver.NXDOMAIN:
        print(f"The domain {dominio} is {Fore.RED}available{Fore.RESET}.")
    except dns.exception.DNSException:
        print(f"{Fore.RED}Error{Fore.RESET} verifying domain {dominio}.")

def show_menu():
    print("Menu:")
    print(f"{RED}1. Ports and Whois Scan{RESET}")
    print(f"{RED}2. Nikto Scan{RESET}")
    print(f"{RED}3. SQL Injection{RESET}")
    print(f"{RED}4. DNS Amplification Scan{RESET}")
    print(f"{RED}5. Analyze Target Domain Info{RESET}")  
    print(f"{RED}6. Osint Domain For Extension{RESET}")
    print(f"{RED}99. Exit{RESET}")


def main():
    if ask_activate_protonvpn():
        # ProtonVPN is activated, you can perform additional actions here if needed.
        pass

    while True:
        show_menu()
        try:
            option = int(input("Choose an option: "))
            if option == 1:
                target_host = input("Enter the IP or URL of the target: ")
                scan_ports_with_nmap(target_host)
                proceed_with_whois = input(f"{ORANGE}Do you want to proceed with Whois information? (y/n): ").lower()
                if proceed_with_whois == 'y':
                    get_whois_info(target_host)
                else:
                    print("Exiting program.")
            elif option == 2:
                target_host = input("Enter the IP or URL of the target: ")
                run_nikto_scan(target_host)
            elif option == 3:
                target_host = input("Enter the IP or URL of the target: ")
                run_sqlmap_scan(target_host)
            elif option == 4:
                target_domain = input("Enter the domain to query: ")
                query_types = ['A', 'NS', 'SOA', 'MX', 'TXT', 'AAAA', 'RRSIG', 'DNSKEY', 'ANY']
                dns_query_with_metasploit(target_domain, query_types)
            elif option == 5:  
                target_domain_url = input("Enter the target domain: ").strip()
                analyze_target_domain_info(target_domain_url)
            elif option == 6:
                nome_dominio = input("Enter the domain name (without protocol and extension): " )
                print(f"{ORANGE}Results:{RESET}")
                cerca_dominio(nome_dominio)
            elif option == 99:
                print("Exiting program.")
                deactivate_protonvpn()  
                break
            else:
                print(f"{RED}Invalid option. Please choose a valid option.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a number.{RESET}")

if __name__ == "__main__":
    main()
