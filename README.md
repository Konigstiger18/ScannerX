Requirements:
Install the requirements with
                    
    python3 installer.py

Run the program with 

    python3 control_panel.py
or using desktop shortcut created by installer script

ScannerX Framework Description:

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

6) Menu option number 6 performs an Open Source Intelligence (OSINT) analysis for the specified domain. Specifically, the user is prompted to enter a domain name (without protocol and extension), and the program checks the availability of various domain extensions. It provides information on which extensions are already registered and which ones are still available. The analysis involves the use of parallel threads to enhance efficiency, and each result is displayed on the screen, indicating whether the domain is registered or available.

7) The XSS scanning module in Python detects and reports potential Cross-Site Scripting vulnerabilities in web pages using predefined payloads and provides detailed output on vulnerability detection. It is a fundamental tool for improving the security of web applications.

8) Exit (Option 99):
Exits the program.
