CRUD de Usuarios + Prueba controlada de Fuerza Bruta (entorno local)

Actividad: CRUD de Usuarios + Prueba controlada de fuerza bruta contra tu propia API (educativa).
Autor: Diego Ruiz 
Alcance: FastAPI backend simple , y script Bash que genera intentos de fuerza bruta únicamente contra localhost.

ADVERTENCIA ÉTICA Y LEGAL
Esta práctica debe realizarse únicamente en entornos de desarrollo/laboratorio y sobre servicios que tú controlas (localhost). No ejecutes ataques contra servicios de terceros ni en producción. Hacerlo puede ser ilegal y dañino.

Contenido del repositorio

main.py — API en FastAPI con endpoints CRUD de usuarios y /login.

bruteforce_api_local.sh — Script Bash para ejecutar una prueba controlada de fuerza bruta contra http://127.0.0.1:8000/login.

README.md — Este archivo.

.gitignore — Ignorar venv/, __pycache__/, etc.

Requisitos (local)

Python 3.9+ (recomendado)

pip

bash (para ejecutar el script)

curl (opcional, para ejemplos)

(opcional) virtualenv / venv

Dependencias Python:

pip install fastapi uvicorn


(O desde un virtualenv:)

python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows (PowerShell: .\venv\Scripts\Activate.ps1)
pip install --upgrade pip
pip install fastapi uvicorn

Ejecutar la API (desarrollo, localhost)

Desde la carpeta donde está main.py:

# con uvicorn (modo desarrollo)
uvicorn main:app --reload --host 127.0.0.1 --port 8000


La API quedará disponible en: http://127.0.0.1:8000

Documentación automática (Swagger UI): http://127.0.0.1:8000/docs
Documentación OpenAPI (ReDoc): http://127.0.0.1:8000/redoc

Endpoints principales (resumen)

Nota: el ejemplo de implementación usa una lista en memoria bd como "base de datos quemada en código".

POST /users/ — Crear usuario (envía JSON con id, username, password, email, is_active).

GET /users — Listar usuarios (parámetros opcionales skip, limit).

GET /users/{id} — Obtener usuario por id.

PUT /users/{id} — Actualizar (no se actualiza password en el ejemplo).

DELETE /users/{id} — Eliminar usuario.

POST /login — Endpoint de autenticación (recibe username y password como form-data y devuelve 200 si coincide).

Ejemplos curl

Crear usuario:

curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"id": 10, "username": "test1", "password": "pass123", "email": "t@t.com", "is_active": true}'


Login (form):

curl -X POST -F "username=test1" -F "password=pass123" http://127.0.0.1:8000/login


Listar usuarios:

curl http://127.0.0.1:8000/users

Script de fuerza bruta (bruteforce_api_local.sh)
Características del script

Generador exhaustivo de contraseñas hasta longitud max_len usando alfabetos seleccionables (digits, alpha, all).

Solo permite targets localhost, 127.0.0.1 o ::1 (protección integrada).

Usa curl y observa el código HTTP; considera 200 como éxito.

Mide intentos y tiempo transcurrido.

Hacer ejecutable
chmod +x bruteforce_api_local.sh

Uso
./bruteforce_api_local.sh <usuario> <max_len> [alphabet] [print_every]


usuario: nombre de usuario objetivo (por ejemplo test1)

max_len: longitud máxima de contraseña a probar (entero)

alphabet (opcional): digits | alpha | all (por defecto digits)

print_every (opcional): imprimir estado cada N intentos (por defecto 1000)

Ejemplo:

# prueba rápida (solo dígitos, longitud hasta 4)
./bruteforce_api_local.sh test1 4 digits 500

Nota importante

El script está pensado para laboratorios y pruebas educativas. No lo ejecutes contra servicios que no controles.

El script verifica que el host del TARGET sea 127.0.0.1 o localhost. Si modificas TARGET, respeta la ley y la ética.

Comportamientos HTTP y cómo lo detecta el script

El script interpreta el código HTTP devuelto por curl:

200 → autenticación exitosa (en tu main.py esa es la respuesta cuando username y password coinciden).

401 → credenciales incorrectas.

403 → usuario inactivo (si aplica).

000 → fallo en la conexión o timeout.

Si quieres que el script compruebe otro criterio (p. ej. contenido del body), deberías modificar la lógica de curl y el test en el script.

Mejoras y recomendaciones de seguridad (imprescindibles para una versión real)

El código provisto NO es seguro para producción. A continuación, medidas necesarias:

Nunca almacenar passwords en texto plano.

Usar hashing seguro (bcrypt, Argon2). Ejemplo con passlib:

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("mi_password")
pwd_context.verify("intento", hashed)


Agregar rate limiting / throttling.

Limitar peticiones por IP / por cuenta. P. ej. slow_down o middleware personalizado.

Bloqueo temporal de cuentas tras N intentos fallidos.

Implementar contador de intentos y bloqueo temporal (exponencial backoff).

Usar HTTPS en entornos reales.

No transmitir credenciales por HTTP sin cifrado.

Autenticación y tokens seguros (JWT / sesiones).

No devolver mensajes inseguros y evitar fugas de información.

Logs y monitorización.

Registrar intentos fallidos/éxitos para auditoría y detección de incidentes.

Validación y saneamiento de entradas.

Evitar inyección o data inconsistente.

Entorno de pruebas separado.

Ejecutar el script y pruebas solo contra entornos identificados y aislados.

Posibles añadidos y ejercicios (recomendados para la práctica)

Reescribir la bd a una SQLite simple con sqlmodel o sqlite3 para persistencia.

Implementar hashing con passlib y cambiar el endpoint de creación para almacenar password hasheado.

Añadir un middleware de rate-limiting (por IP).

Añadir tests automatizados (pytest) que validen la lógica y mitigaciones.

Añadir un endpoint que devuelva estadísticas de intentos (solo admin).

Resumen de comandos útiles

Instalar dependencias:

python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn


Ejecutar API:

uvicorn main:app --reload --host 127.0.0.1 --port 8000


Hacer script ejecutable y lanzarlo:

chmod +x bruteforce_api_local.sh
./bruteforce_api_local.sh test1 4 digits 500


Ejemplo de login con curl:

curl -X POST -F "username=test1" -F "password=pass123" http://127.0.0.1:8000/login -v
