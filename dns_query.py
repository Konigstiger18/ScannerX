import subprocess
from colorama import Fore, Style

# Definizione dei codici di colore
RED = Fore.RED
RESET = Style.RESET_ALL

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

# Esempio di utilizzo
dns_query_with_metasploit("example.com", ["A", "MX", "NS", "ANY", "TXT", "SOA", "AAAA"])
