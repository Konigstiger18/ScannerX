import os
import subprocess
import platform

# Contenuto del file requirements.txt
requirements_content = """
python-nmap
sockets
python-whois
requests
beautifulsoup4
tldextract
colorama
pyfiglet
dnspython
aiohttp
asyncio
urljoin
"""

# Percorso del file requirements.txt
requirements_file_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

# Scrivi il contenuto del file requirements.txt
with open(requirements_file_path, 'w') as f:
    f.write(requirements_content)

# Esegui il comando pip install per installare le dipendenze
try:
    result = subprocess.run(['pip', 'install', '-r', requirements_file_path], check=True, capture_output=True, text=True)
    print(f'Stdout: {result.stdout}')
except subprocess.CalledProcessError as e:
    print(f'Errore durante l\'installazione delle dipendenze: {e.stderr}')
    exit(1)

# Chiedi all'utente se desidera creare un lanciatore sul desktop
create_launcher = input('Vuoi creare un lanciatore sul desktop? (s/N): ').strip().lower() == 's'

if create_launcher:
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    launcher_path = os.path.join(desktop_path, 'ScannerX.desktop')
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')  # Assicurati che l'immagine icon.png sia nella stessa directory di setup.py
    control_panel_path = os.path.join(os.path.dirname(__file__), 'control_panel.py')  # Assicurati che control_panel.py sia nella stessa directory di installer.py

    launcher_content = f"""
[Desktop Entry]
Version=1.0
Type=Application
Name=ScannerX
Exec=python3 /home/kali/Desktop/ScannerX-files/control_panel.py
Icon=/home/kali/Desktop/ScannerX-files/icon.png
Terminal=true

    """

    with open(launcher_path, 'w') as f:
        f.write(launcher_content)

    # Rendi il lanciatore eseguibile
    if platform.system() == 'Linux':
        subprocess.run(['chmod', '+x', launcher_path])

    print('Lanciatore creato sul desktop.')
else:
    print('Lanciatore non creato.')
