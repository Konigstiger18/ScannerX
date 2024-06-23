import aiohttp
import asyncio
import random
import re
import time
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from urllib.parse import urljoin
import os  # Importa il modulo os per gestire i percorsi dei file

# Inizializza colorama
init(autoreset=True)
RED = "\033[91m"
ORANGE = "\033[93m"
RESET = "\033[0m"

# Funzione per leggere i payload da un file
def read_payloads(file_path):
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file.readlines()]
    random.shuffle(payloads)  # Randomizza l'ordine dei payload
    return payloads

# Funzione per pulire e validare i payload
def clean_payload(payload):
    return re.sub(r'[^\x20-\x7E]', '', payload)  # Rimuove caratteri non stampabili

# Funzione per loggare i messaggi con diversi livelli di severità
def log_message(message, level="INFO"):
    levels = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED
    }
    color = levels.get(level, Fore.WHITE)
    print(color + message)

async def fetch(session, url, method='get', data=None, params=None, headers=None, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            if session is not None and callable(getattr(session, 'request', None)):
                async with session.request(method, url, data=data, params=params, headers=headers, timeout=90) as response:
                    return await response.text()
            else:
                log_message("Impossibile creare la sessione o la richiesta.", "ERROR")
                return None
        except aiohttp.ClientError as ce:
            log_message(f"Errore durante l'invio del form: {ce}", "WARNING")
        except asyncio.TimeoutError:
            log_message("Timeout durante l'invio del form", "WARNING")
        except Exception as e:
            log_message(f"Errore durante l'invio del form: {e}", "WARNING")
        attempt += 1
        log_message(f"Retry {attempt}/{retries} per {url}", "WARNING")
        await asyncio.sleep(2)
    return None

async def detect_xss_vulnerabilities(url, payloads, method):
    semaphore = asyncio.Semaphore(5)  # Limita il numero di richieste simultanee
    vulnerable_count = 0  # Contatore per i payload vulnerabili
    total_tested_payloads = 0  # Contatore per i payload testati

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'html.parser')

            # Trova tutti i form nella pagina
            forms = soup.find_all('form')
            log_message(f"{RESET}Trovati {len(forms)} form nella pagina {url}", "INFO")

            total_payloads = len(payloads) * len(forms)
            log_message(f"{RESET}Testando: {total_payloads} ({method.upper()})", "INFO")

            for form in forms:
                action = form.get('action', '')
                action_url = urljoin(url, action)  # Assicurarsi che l'URL sia completo
                inputs = form.find_all(['input', 'textarea', 'select', 'button'])

                log_message(f"\nAnalizzando form con action: {action_url}", "INFO")
                print(f"numero di payloads testati: 0", end='', flush=True)

                form_data = {}
                for input_tag in inputs:
                    input_name = input_tag.get('name')
                    if not input_name:
                        continue

                    input_type = input_tag.get('type', 'text')
                    input_value = input_tag.get('value', '')

                    if input_tag.name == 'select':
                        options = input_tag.find_all('option')
                        for option in options:
                            if option.get('value'):
                                form_data[option.get('name', input_name)] = option['value']
                    elif input_type in ['text', 'textarea', 'hidden', 'submit']:
                        form_data[input_name] = input_value
                    elif input_type == 'checkbox' or input_type == 'radio':
                        if input_tag.has_attr('checked'):
                            form_data[input_name] = input_value
                    elif input_type == 'file':
                        form_data[input_name] = ''  # Placeholder for file inputs, can't be tested via payload

                for payload in payloads:
                    cleaned_payload = clean_payload(payload)
                    for input_name in form_data:
                        original_value = form_data[input_name]
                        form_data[input_name] = cleaned_payload

                        if method == 'post':
                            task = fetch(session, action_url, method='post', data=form_data)
                        else:
                            task = fetch(session, action_url, method='get', params=form_data)
                        
                        response = await bounded_fetch(task, semaphore, delay=0.2)
                        total_tested_payloads += 1

                        # Sovrascrivi la linea corrente con il contatore dei payload testati
                        print(f"{ORANGE}\rNumero di payloads testati: {total_tested_payloads}", end='', flush=True)

                        if response and re.search(re.escape(cleaned_payload), response):
                            # Sovrascrivi la linea corrente con il messaggio di vulnerabilità
                            print(f"\rVulnerabilità trovata: Input {input_name} ({method.upper()}): {cleaned_payload}", flush=True)
                            vulnerable_count += 1
                            # Riprendi la stampa del conteggio sulla stessa riga
                            print(f"{ORANGE}\rNumero di payloads testati: {total_tested_payloads}", end='', flush=True)

                        # Restore original value
                        form_data[input_name] = original_value

    except aiohttp.ClientError as ce:
        log_message(f"Errore durante la richiesta al sito: {ce}", "ERROR")
    except Exception as e:
        log_message(f"Errore durante la richiesta al sito: {e}", "ERROR")

    print()  # Per andare alla riga successiva dopo il conteggio finale
    log_message(f"payloads vulnerabili: {vulnerable_count}", "INFO")
    log_message("Scansione completata.", "INFO")

async def bounded_fetch(task, semaphore, delay=0):
    async with semaphore:
        await asyncio.sleep(delay)  # Introduce un ritardo tra le richieste
        return await task

if __name__ == "__main__":
    try:
        # Chiede l'URL all'utente
        url = input(f"{ORANGE}Inserisci l'URL da analizzare per vulnerabilità XSS: {RESET}")

        # Chiede all'utente quale tipo di scansione vuole eseguire
        print(f"{RED}Seleziona il tipo di scansione:")
        print("1) Veloce")
        print("2) Media")
        print("3) Avanzata")

        scan_type = input("Scelta: ")

        if scan_type == '1':
            payload_file_path = '/home/kali/Desktop/ScanneX-files/xxs/fast-scan.txt'
        elif scan_type == '2':
            payload_file_path = '/home/kali/Desktop/ScanneX-files/xxs/med.txt'
        elif scan_type == '3':
            payload_file_path = '/home/kali/Desktop/ScanneX-files/xxs/advanced.txt'
        else:
            log_message("Opzione di scansione non valida. Scegli tra 1, 2 o 3.", "ERROR")
            exit(1)

        # Verifica se il percorso del file è corretto
        if not os.path.exists(payload_file_path):
            log_message(f"Il file {payload_file_path} non esiste nella directory corrente.", "ERROR")
            exit(1)

        payloads = read_payloads(payload_file_path)

        # Chiede all'utente quale metodo di scansione vuole usare
        print(f"{RED}Seleziona il metodo di scansione:")
        print("1) GET")
        print("2) POST")

        while True:
            method_choice = input("Scelta: ")

            if method_choice == '1':
                method = 'get'
                break
            elif method_choice == '2':
                method = 'post'
                break
            else:
                log_message("Opzione di metodo non valida. Scegli tra 1 o 2.", "ERROR")

        # Stampa il numero di payloads da testare
        log_message(f"{ORANGE}Numero di payloads da testare: {len(payloads)}", "INFO")

        # Esegui la scansione asincrona
        asyncio.run(detect_xss_vulnerabilities(url, payloads, method))

    except KeyboardInterrupt:
        log_message(f"{RED}\nInterruzione del programma richiesta dall'utente.", "WARNING")
        exit(0)
