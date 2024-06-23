import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract

def print_title(title):
    print(f"\033[93m{title}\033[0m")

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

def analyze_target_domain_info(target_domain_url):
    try:
        page_content = get_resource_content(target_domain_url)
        if page_content is None:
            return
        soup = BeautifulSoup(page_content, 'html.parser')

        print_title(f"Login pages for {target_domain_url}")
        login_pages = find_login_pages(soup, target_domain_url)
        print(login_pages)

        print_title(f"Robots.txt content for {target_domain_url}")
        robots_txt_url = find_robots_txt_url(target_domain_url)
        robots_txt_content = get_robots_txt_content(robots_txt_url) if robots_txt_url else "File robots.txt not found"
        print(robots_txt_content)

        print_title(f"Subdomains for {target_domain_url}")
        subdomains = find_subdomains(target_domain_url)
        print(subdomains)
    except Exception as e:
        print(f"Error analyzing target domain: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze information of a target domain.")
    parser.add_argument('target_domain_url', help="The target domain URL.")
    
    args = parser.parse_args()
    analyze_target_domain_info(args.target_domain_url)
