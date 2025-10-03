# CRUD de Usuarios + Prueba Controlada de Fuerza Bruta (Entorno de laboratorio)

> **Actividad (educativa):** implementar una API REST con operaciones CRUD sobre usuarios y, de forma controlada y ética, ejecutar un experimento de fuerza bruta contra **tu propia** API de desarrollo para comprender vulnerabilidades y diseñar medidas de mitigación.  
> **Importante:** todas las pruebas deben realizarse **únicamente** en entornos de desarrollo / laboratorio y con cuentas creadas expresamente para la práctica. Nunca ataques sistemas de terceros.

---

## Índice
1. [Objetivo](#objetivo)  
2. [Requisitos](#requisitos)  
3. [Instalación y puesta en marcha](#instalación-y-puesta-en-marcha)  
4. [Endpoints (resumen)](#endpoints-resumen)  
5. [Usuarios de prueba incluidos](#usuarios-de-prueba-incluidos)  
6. [Ejemplos `curl` (pruebas manuales)](#ejemplos-curl-pruebas-manuales)  
7. [Ejecutar la prueba controlada de fuerza bruta (laboratorio)](#ejecutar-la-prueba-controlada-de-fuerza-bruta-laboratorio)  
8. [Mediciones y registro (qué anotar)](#mediciones-y-registro-qué-anotar)  
9. [Resultados esperables y análisis](#resultados-esperables-y-análisis)  
10. [Medidas de mitigación recomendadas](#medidas-de-mitigación-recomendadas)  
11. [Checklist de entrega](#checklist-de-entrega)  
12. [Advertencias de seguridad y ética](#advertencias-de-seguridad-y-ética)  
13. [requirements.txt](#requirementstxt)  
14. [Autor](#autor)

---

## Objetivo
- Diseñar e implementar endpoints CRUD seguros para `Usuario`.  
- Comprender cómo un ataque de fuerza bruta puede explotar credenciales débiles.  
- Medir recursos y efectos del experimento.  
- Justificar estadísticas y proponer mitigaciones.

---

## Requisitos
- Python 3.8+  
- `pip`  
- (Opcional) `jq` para formatear JSON en la terminal  
- Entorno local / máquina propia para ejecutar la API

---

## Instalación y puesta en marcha

1. Clona el repositorio (si aplica):
```bash
git clone https://github.com/TU-USUARIO/mi-repo.git
cd mi-repo
Crear y activar entorno virtual:
python3 -m venv venv
source venv/bin/activate    # Linux / macOS
# o en Windows PowerShell:
# .\venv\Scripts\Activate.ps1

Instalar dependencias desde requirements.txt:
pip install -r requirements.txt

Ejecutar la API (modo desarrollo):
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API disponible en: http://127.0.0.1:8000

Swagger UI (docs): http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Endpoints (resumen)
Método	Ruta	Descripción	Payload / Notes
GET	/	Mensaje de salud	—
GET	/users	Listar usuarios (opcional skip, limit)	Query params
GET	/users/{id}	Obtener usuario por id	—
POST	/users/	Crear usuario	JSON {id, username, password, email?, is_active?}
PUT	/users/{id}	Actualizar usuario (no password)	JSON con campos a actualizar
DELETE	/users/{id}	Eliminar usuario	—
POST	/login	Autenticación (form-data)	Form: username, password

Nota: En este proyecto, por simplicidad, las contraseñas se almacenan en texto plano en memoria solo para fines educativos. En producción se debe usar hashing seguro.

Usuarios de prueba incluidos
id	username	password	email
1	testuser	123	test@example.com
2	diegosantillan625@gmail.com	123456789	diegosantillan625@gmail.com
3	juanperez	abc123	test@yo.com
4	diego	abc	yo@yo.com

Usa estas cuentas solo en tu entorno de laboratorio.

Ejemplos curl (pruebas manuales)

Listar usuarios:
curl -s http://127.0.0.1:8000/users | jq

Obtener usuario (id=1):
curl -s http://127.0.0.1:8000/users/1 | jq

Crear usuario:
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"id":5,"username":"prueba","password":"pw","email":"a@a.com","is_active":true}' \
  http://127.0.0.1:8000/users/ | jq

Actualizar usuario:
curl -s -X PUT -H "Content-Type: application/json" \
  -d '{"id":1,"username":"testuser","email":"new@example.com","is_active":true}' \
  http://127.0.0.1:8000/users/1 | jq

Eliminar usuario:
curl -s -X DELETE http://127.0.0.1:8000/users/1 | jq

Login (form-encoded):
curl -s -X POST -F "username=diego" -F "password=abc" http://127.0.0.1:8000/login
Ejecutar la prueba controlada de fuerza bruta (laboratorio)
Reglas obligatorias:

Ejecutar solo en tu entorno local/lab.

Usar únicamente cuentas de prueba creadas para la práctica.

Limitar espacio de búsqueda y velocidad (por ejemplo: digits, max_len <= 3).

Registrar métricas y resultados.

Opción A — Script Python interactivo (ejemplo incluido)

Activa el entorno virtual:
source venv/bin/activate

Ejecuta:
python3 bruteforce.py
Cuando pregunte, introduce:

less
Copiar código
Usuario objetivo: diego
Longitud máxima (ej. 3): 3
Alfabeto (digits|alpha|all) [digits]: digits
Imprimir cada N intentos [1000]: 100
Opción B — Wrapper bash (si existe bruteforcebash.sh)
chmod +x bruteforcebash.sh
./bruteforcebash.sh
Recomendaciones de seguridad durante la ejecución
Empezar con max_len = 1 o 2 para confirmar comportamiento.

Añadir sleep entre intentos si el script lo permite (reduce impacto).

No dejar scripts en ejecución larga sin supervisión.

Mediciones y registro (qué anotar)
Durante la prueba anota:

Métrica	Por qué
Usuario objetivo	identificación del caso de prueba
Parámetros (alfabeto, max_len, print_every, sleep)	reproducc. del experimento
Hora inicio / fin	calcular duración
Intentos totales	coste en recursos
Resultado (contraseña encontrada / no encontrada)	objetivo
Códigos HTTP (fallo / éxito)	comprobar comportamiento del servidor
Latencia media por petición	impacto en performance
Uso CPU / memoria (opcional)	efecto en servidor

Sugerencia de log CSV:

makefile
timestamp,attempts,username,candidate,http_code,elapsed_seconds
2025-10-03T22:15:00,120,diego,007,401,0.035
Resultados esperables y análisis
Contraseñas débiles (cortas / solo dígitos) suelen descubrirse muy rápido.

El tiempo crece exponencialmente con la longitud y el tamaño del alfabeto.

Con medidas defensivas (rate limit, lockout) el éxito del ataque se reduce o se vuelve impracticable.

Analiza y documenta: intentos hasta éxito, tiempo total y cualquier bloqueo observado.

Medidas de mitigación recomendadas
Hash de contraseñas (bcrypt/argon2) antes de almacenar.

Política de contraseñas (longitud mínima, blacklist de contraseñas comunes).

Rate limiting por IP/usuario.

Lockout temporal tras N intentos fallidos.

MFA para cuentas sensibles.

TLS/HTTPS en producción.

No revelar en mensajes si el usuario existe o no.

Monitoreo y alertas ante patrones de fuerza bruta.

Tests automáticos que verifiquen bloqueo y políticas de seguridad.

Checklist de entrega
 Código de la API (main.py) y demás fuentes.

 requirements.txt.

 Scripts de prueba (bruteforce.py, bruteforcebash.sh) — solo para uso en laboratorio.

 Logs/CSV con resultados de la prueba.

 Informe con análisis, gráficos y propuestas de mitigación.

Advertencias de seguridad y ética
Ejecuta pruebas solo en entornos propios o con autorización explícita.

No realices ataques contra terceros.

Documenta y limita el experimento para evitar impacto no deseado.

No uses datos reales ni contraseñas reales en las pruebas.

requirements.txt (recomendado)
Incluye este archivo en la raíz del proyecto con, al menos, estas dependencias:

makefile
fastapi==0.95.2
uvicorn[standard]==0.23.1
pydantic==1.10.12
requests==2.31.0
python-multipart==0.0.6
Ajusta versiones según tu entorno.

Autor
Diego Ruiz
Universidad Internacional del Ecuador (UIDE)
Proyecto académico — Seguridad informática y APIs con FastAPI
Quito, Ecuador — 2025

