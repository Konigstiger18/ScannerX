import dns.resolver
import dns.exception
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style

def cerca_dominio(nome_dominio):
    estensioni = [
        # Lista delle estensioni di dominio da verificare
        ".com", ".net", ".org", ".gov", ".edu", ".biz", ".info", ".name", ".pro", ".mobi", ".int", ".coop", ".aero", ".travel",
        ".it", ".fr", ".es", ".de", ".uk", ".us", ".ca", ".au", ".jp", ".cn", ".br", ".ru",
        ".in", ".mx", ".nl", ".nz", ".se", ".ch", ".za", ".ae", ".sa", ".ar", ".id", ".tr",
        ".io", ".ai", ".app", ".dev", ".tech", ".systems", ".web", ".software", ".code", ".data", ".network", ".cloud",
        ".blog", ".news", ".info", ".media", ".tv", ".movie", ".music", ".gaming", ".art", ".photo", ".gallery", ".studio",
        ".store", ".shop", ".market", ".online", ".sale", ".buy", ".discount", ".shop", ".fashion", ".jewelry", ".food", ".restaurant",
        ".guru", ".expert", ".consulting", ".lawyer", ".doctor", ".engineer", ".architect", ".accountant",
        ".dentist", ".realty", ".consultant", ".coach", ".therapy", ".training", ".education", ".academy",
        ".co", ".me", ".xyz", ".space", ".club", ".live", ".link", ".social", ".design", ".events", ".travel", ".party", ".golf",
        ".fitness", ".photography", ".blog", ".gaming", ".family", ".pet", ".science", ".green", ".eco",
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(verifica_dominio, f"{nome_dominio}{estensione}") for estensione in estensioni]
        for future in futures:
            future.result()

def verifica_dominio(dominio):
    try:
        answers = dns.resolver.resolve(dominio, 'A')
        print(f"The domain {dominio} is {Fore.GREEN}registered{Style.RESET_ALL}.")
    except dns.resolver.NXDOMAIN:
        print(f"The domain {dominio} is {Fore.RED}available{Style.RESET_ALL}.")
    except dns.exception.DNSException:
        print(f"{Fore.RED}Error{Style.RESET_ALL} verifying domain {dominio}.")

# Esempio di utilizzo
cerca_dominio("example")
