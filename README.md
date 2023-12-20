Requirements:

For Debian/Ubuntu/Kali Linux:

    sudo apt update
    sudo apt install python
    pip install python-nmap
    pip install python-whois
    pip install requests
    pip install beautifulsoup4
    pip install tldextract
    pip install colorama
    pip install pyfiglet

For Arch Linux:

    sudo pacman -Syu
    sudo pacman -S python
    pip install python-nmap
    pip install python-whois
    pip install requests
    pip install beautifulsoup4
    pip install tldextract
    pip install colorama
    pip install pyfiglet

ScannerX Tool Description:

 1) Ports and Whois Scan (Option 1):
Prompts the user to enter the IP or URL of the target.
Performs a port scan using Nmap on the specified target.
Optionally, retrieves and displays Whois information for the target.

The whois module in Python provides various pieces of information when executing the whois.whois(target) function. Here are some common pieces of information that can be obtained through the whois module:

   IP Address:
        The IP address of the website associated with the domain.

   Hosting Location:
        Hosting location, which may include city, region, and country.

   Registrar:
        The entity with which the domain is registered.

   Registrar Abuse Email:
        The email address associated with reporting abuse to the registrar.

   Registrant Email:
        The email address of the domain registrant.

   Creation Date:
        The date when the domain was created.

   Expiration Date:
        The date when the domain is set to expire.

   Cloudflare:
        Indicates whether the website uses Cloudflare for protection.

   Name Servers:
        A list of name servers associated with the domain.

   Status:
        The current status of the domain, such as active, inactive, etc.

2) Nikto Scan (Option 2):
Prompts the user to enter the IP or URL of the target.
Runs a Nikto scan on the specified target to identify potential vulnerabilities.

3) SQL Injection (Option 3):
Prompts the user to enter the IP or URL of the target.
Executes a SQLmap scan on the specified target to detect SQL injection vulnerabilities.

4) DNS Amplification Scan (Option 4):
 Prompts the user to enter the domain to query.
 Performs automatized DNS queries using Metasploit for various record types (A, NS, SOA, MX, TXT, AAAA, RRSIG, DNSKEY, ANY).

5) Analyze Target Domain Info (Option 5):
Prompts the user to enter the target domain.
Fetches and displays information about the target domain, including login pages, robots.txt content, and subdomains.

6) Exit (Option 99):
Exits the program.
If ProtonVPN was activated at the beginning, it also deactivates ProtonVPN.

If you want support my project: https://www.paypal.me/konig18?locale.x=it_IT
