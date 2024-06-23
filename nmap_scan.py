import subprocess

def scan_ports_with_nmap(target):
    print("Scanning ports...\n")
    try:
        nmap_command = f"nmap -T3 -p 1-1000 {target}"
        subprocess.call(nmap_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Nmap scan failed: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perform a port scan using Nmap.")
    parser.add_argument('target', help="The IP or URL of the target.")
    
    args = parser.parse_args()
    scan_ports_with_nmap(args.target)
