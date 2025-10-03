# CRUD de Usuarios + Prueba controlada de Fuerza Bruta (entorno local)

## Descripción (breve)
API educativa en **FastAPI** que implementa operaciones CRUD sobre usuarios y un script Bash que realiza pruebas controladas de fuerza bruta **únicamente** en `localhost`. Ejecutar siempre en entornos de laboratorio.

> **Advertencia:** todas las pruebas deben ejecutarse exclusivamente en entornos de desarrollo/laboratorio y sobre servicios que usted controla. Ejecutar ataques contra terceros es ilegal y poco ético.

---

## Estructura importante

| Archivo / Carpeta | Descripción |
|---|---|
| `main.py` | API en FastAPI. Lista en memoria `bd` (simula base de datos). |
| `bruteforce_api_local.sh` | Script Bash para probar fuerza bruta contra `POST /login` en `localhost`. |
| `.gitignore` | Reglas para excluir `venv/`, `__pycache__/`, y archivos temporales. |
| `README.md` | Este documento (instrucciones y ejemplos). |

---

## Requisitos mínimos

| Elemento | Requisito |
|---|---|
| Python | 3.9+ |
| pip | Recomendado actualizar a la última versión |
| Shell | `bash` (Linux/macOS o Git Bash en Windows) |
| curl | Opcional (para pruebas) |
| Entorno virtual | Recomendado (`venv`) |

Instalar dependencias (rápido):
```bash
pip install fastapi uvicorn
Instalación rápida
bash
Copiar código
git clone https://github.com/TU-USUARIO/mi-repo.git
cd mi-repo

# (Opcional) crear y activar entorno virtual
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install fastapi uvicorn
Ejecutar la API (local)
bash
Copiar código
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Modelo de datos (resumen)
Campo	Tipo	Observaciones
id	int	Identificador numérico
username	str	Debe ser único (en diseño ideal)
password	str	Texto plano en el ejemplo — no apto para producción
email	str (opcional)	Correo del usuario
is_active	bool	Cuenta activa/inactiva

Actualmente los usuarios se almacenan en la lista en memoria bd. Para persistencia, migrar a SQLite u otra base de datos.

##Endpoints (resumen)
Método	Ruta	Descripción
POST	/users/	Crear usuario (JSON)
GET	/users	Listar usuarios (skip, limit)
GET	/users/{id}	Obtener usuario por id
PUT	/users/{id}	Actualizar usuario (ejemplo no actualiza password)
DELETE	/users/{id}	Eliminar usuario
POST	/login	Autenticar (form-data: username, password)

Ejemplos (bloques de código)
Crear usuario
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"id":10,"username":"t","password":"p","email":"a@b.com","is_active":true}'
Listar usuarios
curl http://127.0.0.1:8000/users

Obtener usuario por id
curl http://127.0.0.1:8000/users/1

Actualizar usuario
curl -X PUT "http://127.0.0.1:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"id":1,"username":"nuevo","password":"x","email":"e@e.com","is_active":true}'

Eliminar usuario
curl -X DELETE http://127.0.0.1:8000/users/1

Login (form-data)
curl -X POST -F "username=t" -F "password=p" http://127.0.0.1:8000/login

Script de fuerza bruta — bruteforce_api_local.sh
Propósito: generar combinaciones de contraseñas y probarlas contra POST /login en localhost. El script valida que el TARGET sea 127.0.0.1 / localhost / ::1.

Uso rápido
chmod +x bruteforce_api_local.sh
./bruteforce_api_local.sh <usuario> <max_len> [alphabet] [print_every]

Parámetros

Parámetro	Descripción	Ejemplo
usuario	Usuario objetivo	test1
max_len	Longitud máxima de contraseña a probar (entero)	4
alphabet	digits | alpha | all (por defecto digits)	digits
print_every	Mostrar estado cada N intentos (por defecto 1000)	500

Ejemplo:

./bruteforce_api_local.sh test1 4 digits 500
Interpretación rápida de códigos HTTP
Código	Significado
200	Login exitoso (ataque: contraseña encontrada)
401	Credenciales incorrectas
403	Usuario inactivo
000	Fallo de conexión / timeout

Riesgos y recomendaciones de seguridad
Resumen: este proyecto es pedagógico. No usar en producción sin aplicar medidas de seguridad.

Medidas críticas (mínimas antes de producción)
Medida	Por qué	Prioridad
Hashing de contraseñas (bcrypt/Argon2)	Evita exposición si la BD se filtra	Imprescindible
Rate limiting (por IP/usuario)	Reduce velocidad de ataques automatizados	Imprescindible
Bloqueo temporal tras N intentos	Evita ataques continuos / enumeración	Altamente recomendado
HTTPS/TLS	Cifra credenciales en tránsito	Imprescindible
Logging y alertas	Detección temprana de actividad sospechosa	Altamente recomendado
Separar entornos (dev/test/prod)	Evita impacto en producción durante pruebas	Altamente recomendado

Parámetros de endurecimiento sugeridos (ejemplo)
Parámetro	Valor sugerido
Intentos fallidos antes de bloqueo	5
Duración bloqueo inicial	15 minutos
Política de backoff	Exponencial (doblar espera por bloqueos sucesivos)
Límite por IP	20 req/min (ajustable según carga)
Hashing	bcrypt (cost >= 12) o Argon2

Ejemplo de hashing con passlib (Python)
python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashear antes de almacenar
hashed = pwd_context.hash("mi_password")

# Verificar en login
if pwd_context.verify("intento", hashed):
    # contraseña correcta
    pass
Mejoras sugeridas (prioridad)
Prioridad	Mejora
Alta	Persistencia con SQLite (sqlmodel / sqlite3) y almacenar passwords hasheadas
Alta	Implementar middleware de rate-limiting
Media	Contador y bloqueo por intentos fallidos (persistente)
Media	Autenticación con tokens (JWT)
Baja	Endpoint de auditoría / métricas (solo admin)
Baja	Tests automatizados con pytest

Comandos útiles (resumen)
Crear entorno e instalar dependencias
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install fastapi uvicorn

Ejecutar API
uvicorn main:app --reload --host 127.0.0.1 --port 8000

Ejecutar script de fuerza bruta
chmod +x bruteforce_api_local.sh
./bruteforce_api_local.sh test1 4 digits 500

Git (agregar, commit y push)
git add README.md .gitignore main.py bruteforce_api_local.sh
git commit -m "Actualizar README y añadir API y script de prueba"
git pull --rebase origin main   # sincronizar antes de push si el remoto tiene cambios
git push -u origin main

Créditos
Diego Ruiz
