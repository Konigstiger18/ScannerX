import socket
import whois
import requests

def format_dates(dates):
    if isinstance(dates, list):
        return "\n".join(date.strftime("%Y-%m-%d %H:%M:%S") for date in dates)
    else:
        return dates.strftime("%Y-%m-%d %H:%M:%S") if dates else "N/A"

def format_list(items):
    return "\n".join(items) if items else "N/A"

def get_abuse_email_registrar(whois_info):
    abuse_keywords = ["abuse", "report_abuse", "contact", "abuse_contact"]
    for key, value in whois_info.items():
        key_lower = key.lower()
        value_lower = str(value).lower()
        for keyword in abuse_keywords:
            if keyword in key_lower or keyword in value_lower:
                return value
    return "N/A"

def check_cloudflare(target):
    try:
        response = requests.get(f'http://{target}', timeout=5)
        return 'cloudflare' in response.headers.get('server', '').lower()
    except requests.RequestException:
        return False

def get_hosting_location(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'fail':
            print("Failed to retrieve hosting location information.")
            return 'N/A'
        city = data.get('city', 'N/A')
        region = data.get('regionName', 'N/A')
        country = data.get('country', 'N/A')
        return f"{city}, {region}, {country}"
    except (socket.gaierror, requests.RequestException) as e:
        print(f"Error: {e}")
        return 'N/A'

def get_whois_info(target):
    try:
        ip_address_site = socket.gethostbyname(target)
        is_cloudflare = check_cloudflare(target)
        w = whois.whois(target)
        print(f"IP Address:\n{ip_address_site}")
        print(f"Hosting Location: {get_hosting_location(target)}")
        print(f"Registrar:\n{w.registrar}")
        print(f"Registrar Abuse Email:\n{get_abuse_email_registrar(w)}")
        print(f"Registrant Email:\n{w.get('email', 'N/A')}")
        print(f"Creation Date:\n{format_dates(w.creation_date)}")
        print(f"Expiration Date:\n{format_dates(w.expiration_date)}")
        print(f"Cloudflare: {'Yes' if is_cloudflare else 'No'}")
        print(f"Name Servers:\n{format_list(w.name_servers)}")
        print(f"Status:\n{', '.join(w.status)}")
    except (whois.parser.PywhoisError, socket.error) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retrieve Whois information for a domain.")
    parser.add_argument('target', help="The domain name.")
    
    args = parser.parse_args()
    get_whois_info(args.target)
