# CRUD de Usuarios + Prueba controlada de Fuerza Bruta (entorno local)

## Descripción
Proyecto educativo que implementa una API REST con operaciones CRUD sobre usuarios (FastAPI) y un script Bash para realizar, de forma controlada y ética, una prueba de fuerza bruta contra el endpoint de autenticación propio. El objetivo es entender vulnerabilidades derivadas de credenciales débiles, medir impacto en un entorno controlado y aprender medidas de mitigación.

> **Advertencia:** todas las pruebas deben ejecutarse exclusivamente en entornos de desarrollo/laboratorio y sobre servicios que usted controla. Ejecutar ataques contra terceros es ilegal y poco ético.

---

## Estructura del repositorio

| Archivo / Carpeta | Descripción |
|---|---|
| `main.py` | Código de la API (FastAPI). Lista en memoria usada como "BD". |
| `bruteforce_api_local.sh` | Script Bash para probar fuerza bruta contra `POST /login` en `localhost`. |
| `.gitignore` | Reglas para evitar subir entornos virtuales, cachés y archivos temporales. |
| `README.md` | Documento de uso e instrucciones (este archivo). |

---

## Requisitos (local)

- Python 3.9+  
- `pip`  
- `bash` (Linux / macOS / Git Bash en Windows)  
- `curl` (opcional, para pruebas)  

Dependencias Python:
```bash
pip install fastapi uvicorn
Se recomienda el uso de un entorno virtual (venv).

Instalación y preparación
Clonar el repositorio:

bash
Copiar código
git clone https://github.com/TU-USUARIO/mi-repo.git
cd mi-repo
Crear y activar entorno virtual (opcional pero recomendado):

bash
Copiar código
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
Instalar dependencias:

bash
Copiar código
pip install --upgrade pip
pip install fastapi uvicorn
Ejecutar la API (entorno local)
En la raíz del proyecto:

bash
Copiar código
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Modelo de datos (resumen)
Campo	Tipo	Observaciones
id	int	Identificador numérico del usuario
username	str	Debe ser único en diseño ideal
password	str	En el ejemplo se almacena en texto plano — no apto para producción
email	str (opcional)	Correo electrónico del usuario
is_active	bool	Indicador de cuenta activa/inactiva

En la implementación actual los usuarios se guardan en la lista en memoria bd. Para persistencia, cambie a SQLite o similar.

Endpoints (resumen con ejemplo)
Método	Ruta	Descripción	Ejemplo (curl)
POST	/users/	Crear usuario (JSON).	curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"id":10,"username":"t","password":"p","email":"a@b.com","is_active":true}'
GET	/users	Listar usuarios (skip, limit).	curl http://127.0.0.1:8000/users
GET	/users/{id}	Obtener usuario por id.	curl http://127.0.0.1:8000/users/1
PUT	/users/{id}	Actualizar usuario (no actualiza password en ejemplo).	curl -X PUT -H "Content-Type: application/json" -d '{"id":1,"username":"nuevo","password":"x","email":"e@e.com","is_active":true}' http://127.0.0.1:8000/users/1
DELETE	/users/{id}	Eliminar usuario.	curl -X DELETE http://127.0.0.1:8000/users/1
POST	/login	Autenticar (form-data username, password).	curl -X POST -F "username=t" -F "password=p" http://127.0.0.1:8000/login

Script de fuerza bruta: bruteforce_api_local.sh
Propósito
Generar combinaciones de contraseñas y probarlas contra POST /login en localhost. Protecciones integradas obligan TARGET a 127.0.0.1 / localhost / ::1.

Hacerlo ejecutable
bash
Copiar código
chmod +x bruteforce_api_local.sh
Uso
bash
Copiar código
./bruteforce_api_local.sh <usuario> <max_len> [alphabet] [print_every]
Parámetro	Descripción	Ejemplo
usuario	Nombre del usuario objetivo	test1
max_len	Longitud máxima de contraseña a probar (entero)	4
alphabet	digits | alpha | all (por defecto digits)	digits
print_every	Mostrar estado cada N intentos (por defecto 1000)	500

Ejemplo:

bash
Copiar código
./bruteforce_api_local.sh test1 4 digits 500
Interpretación de códigos HTTP
200 — login exitoso (script lo marca como encontrado).

401 — credenciales incorrectas.

403 — usuario inactivo.

000 — fallo en la conexión o timeout.

Riesgos y recomendaciones de seguridad
Resumen: el ejemplo es pedagógico; no use este diseño en producción sin aplicar las medidas listadas abajo.

Medidas críticas (mínimas a implementar antes de producción)
Medida	Por qué	Nivel (imprescindible/altamente recomendado)
Hashing de contraseñas (bcrypt/Argon2)	Evita exposición de credenciales si la BD se filtra	Imprescindible
Rate limiting por IP/usuario	Reduce la velocidad de ataques automatizados	Imprescindible
Bloqueo temporal tras N intentos	Previene enumeración/ataques continuos	Altamente recomendado
HTTPS/TLS	Cifra credenciales en tránsito	Imprescindible
Registro y alertas	Detección y respuesta temprana a ataques	Altamente recomendado
Separar entornos (dev/test/prod)	Evitar impacto en producción durante pruebas	Altamente recomendado

Ejemplo de hashing con passlib (Python)
python
Copiar código
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashear antes de almacenar
hashed = pwd_context.hash("mi_password")

# Verificar en login
if pwd_context.verify("intento", hashed):
    # contraseña correcta
    pass
Mejoras sugeridas (ejercicios prácticos)
Persistencia con SQLite (sqlmodel o sqlite3) en lugar de lista en memoria.

Almacenar password hasheada (ver arriba).

Implementar rate limiting (por IP y por usuario).

Contador y bloqueo temporal tras N intentos fallidos (p. ej. 5 intentos ⇒ bloqueo 15 min).

Cambiar POST /login para devolver tokens (JWT) en lugar de mensajes simples.

Añadir logs y endpoint de auditoría (solo admin).

Tests automáticos con pytest para endpoints principales y mitigaciones.

Comandos útiles (resumen)
Instalación y entorno:

bash
Copiar código
python -m venv venv
source venv/bin/activate        # Linux/macOS
# .\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install --upgrade pip
pip install fastapi uvicorn
Ejecutar API:

bash
Copiar código
uvicorn main:app --reload --host 127.0.0.1 --port 8000
Ejecutar script de fuerza bruta:

bash
Copiar código
chmod +x bruteforce_api_local.sh
./bruteforce_api_local.sh test1 4 digits 500
Git (agregar README y .gitignore, commit y push):

bash
Copiar código
git add README.md .gitignore main.py bruteforce_api_local.sh
git commit -m "Agregar README, .gitignore, API y script de prueba"
# Primero sincronizar cambios remotos (si aplica)
git pull --rebase origin main
git push -u origin main
Créditos
Diego Ruiz

Copiar código
