import subprocess

def run_sqlmap_scan(target):
    try:
        print(f"Running SQLmap scan on {target}...")
        sqlmap_command = f"sqlmap -u {target}"
        subprocess.call(sqlmap_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running SQLmap scan: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perform a scan using SQLmap.")
    parser.add_argument('target', help="The URL of the target.")
    
    args = parser.parse_args()
    run_sqlmap_scan(args.target)
