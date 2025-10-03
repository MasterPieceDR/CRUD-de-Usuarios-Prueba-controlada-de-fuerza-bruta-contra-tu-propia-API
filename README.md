# CRUD de Usuarios + Prueba controlada de Fuerza Bruta (entorno local)

## Descripción
Proyecto educativo que implementa una API REST con operaciones CRUD sobre usuarios (FastAPI) y un script Bash para realizar, de forma controlada y ética, una prueba de fuerza bruta contra el endpoint de autenticación propio. El propósito es comprender vulnerabilidades básicas (credenciales débiles), medir impacto y diseñar contramedidas.

> Advertencia: todas las pruebas deben realizarse exclusivamente en entornos de desarrollo/laboratorio y sobre servicios que usted controla. Ejecutar ataques contra terceros es ilegal y poco ético.

---

## Contenido del repositorio
- `main.py`  
  Código de la API en FastAPI (lista en memoria como "base de datos").
- `bruteforce_api_local.sh`  
  Script Bash para ejecutar intentos de fuerza bruta contra `http://127.0.0.1:8000/login`.
- `.gitignore`  
  Archivo para excluir `venv/`, `__pycache__/`, etc.
- `README.md`  
  Este documento.

---

## Requisitos
- Python 3.9+  
- `pip`  
- `bash` (Linux / macOS / Git Bash en Windows)  
- `curl` (opcional, para ejemplos)  

Dependencias Python:
```bash
pip install fastapi uvicorn
Se recomienda usar un entorno virtual (venv).

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
En la raíz del proyecto, ejecutar:

bash
Copiar código
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API disponible en: http://127.0.0.1:8000

Documentación automática (Swagger): http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Modelo de datos (ejemplo)
El proyecto utiliza un modelo Usuario con los campos mínimos:

id (int)

username (str, único en el diseño esperado)

password (str) — en el ejemplo se almacena en texto plano (no apto para producción)

email (opcional)

is_active (bool)

En la implementación actual, los usuarios se guardan en una lista en memoria (bd) que actúa como base de datos temporal.

Endpoints principales
POST /users/ — Crear usuario (JSON con id, username, password, email, is_active).

GET /users — Listar usuarios (opciones skip y limit).

GET /users/{id} — Obtener usuario por id.

PUT /users/{id} — Actualizar usuario (en el ejemplo no se actualiza password).

DELETE /users/{id} — Eliminar usuario.

POST /login — Autenticar usuario (recibe username y password como form-data).

Ejemplos de uso con curl
Crear usuario:

bash
Copiar código
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "username": "test1", "password": "pass123", "email": "t@t.com", "is_active": true}'
Listar usuarios:

bash
Copiar código
curl http://127.0.0.1:8000/users
Obtener usuario por id:

bash
Copiar código
curl http://127.0.0.1:8000/users/1
Login (form-data):

bash
Copiar código
curl -X POST -F "username=test1" -F "password=pass123" http://127.0.0.1:8000/login
Eliminar usuario:

bash
Copiar código
curl -X DELETE http://127.0.0.1:8000/users/10
Script de fuerza bruta (bruteforce_api_local.sh)
Propósito
Generar combinaciones de contraseñas y enviarlas al endpoint /login local para observar respuestas y tiempos. El script incluye protecciones para prevenir ataques remotos: por defecto solo permite 127.0.0.1, localhost y ::1.

Hacer ejecutable
bash
Copiar código
chmod +x bruteforce_api_local.sh
Uso
bash
Copiar código
./bruteforce_api_local.sh <usuario> <max_len> [alphabet] [print_every]
Parámetros:

<usuario>: usuario objetivo (por ejemplo test1)

<max_len>: longitud máxima de contraseña a probar (entero)

[alphabet]: digits | alpha | all (por defecto digits)

[print_every]: imprimir estado cada N intentos (por defecto 1000)

Ejemplo:

bash
Copiar código
./bruteforce_api_local.sh test1 4 digits 500
Código de retorno y detección
El script considera HTTP 200 como éxito (login correcto). Otros códigos (401, 403) indican fallo o usuario inactivo. 000 indica problemas de conexión o timeout.

Riesgos y recomendaciones de seguridad
La implementación del ejemplo no es segura para producción. Recomendaciones imprescindibles antes de usar en entornos reales:

No almacenar contraseñas en texto plano. Utilizar hashing (bcrypt, Argon2). Ejemplo con passlib:

python
Copiar código
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("mi_password")
pwd_context.verify("intento", hashed)
Rate limiting / throttling. Implementar límites por IP y por cuenta para mitigar intentos automatizados.

Bloqueo temporal tras N intentos fallidos. Usar backoff exponencial o bloqueos temporales por cuenta/IP.

Usar HTTPS para cifrar credenciales en tránsito.

Auditoría y alertas. Registrar intentos de autenticación fallida y disparar alertas si se detecta actividad sospechosa.

Separar entornos de pruebas y producción. Ejecutar pruebas solo en entornos controlados y aislados.

Posibles mejoras (ejercicios recomendados)
Persistencia: cambiar la lista en memoria a SQLite (sqlmodel o sqlite3).

Hashing de contraseñas durante creación y verificación.

Implementar middleware de rate-limiting.

Añadir autenticación basada en tokens (por ejemplo JWT).

Implementar tests automatizados (pytest) y métricas de rendimiento.

Comandos útiles resumen
Instalación:

bash
Copiar código
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn
Ejecutar API:

bash
Copiar código
uvicorn main:app --reload --host 127.0.0.1 --port 8000
Permitir ejecución del script y lanzarlo:

bash
Copiar código
chmod +x bruteforce_api_local.sh
./bruteforce_api_local.sh test1 4 digits 500
Licencia
Indique la licencia deseada (por ejemplo MIT). Añada un archivo LICENSE si corresponde.

Contacto / Créditos
Proyecto y ejemplos: Diego Ruiz 
