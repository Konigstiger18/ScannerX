import subprocess

def run_nikto_scan(target):
    try:
        print(f"Running Nikto scan on {target}...")
        nikto_command = f"nikto -h {target}"
        subprocess.call(nikto_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Nikto scan: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perform a scan using Nikto.")
    parser.add_argument('target', help="The IP or URL of the target.")
    
    args = parser.parse_args()
    run_nikto_scan(args.target)
