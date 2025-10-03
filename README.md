<!-- README.md con anclas explícitas antes de cada encabezado -->

# CRUD de Usuarios + Prueba Controlada de Fuerza Bruta (Entorno de laboratorio)

> **Actividad (educativa):** implementar una API REST con operaciones CRUD sobre usuarios y, de forma controlada y ética, ejecutar un experimento de fuerza bruta contra **tu propia** API de desarrollo para comprender vulnerabilidades y diseñar medidas de mitigación.  
> **Importante:** todas las pruebas deben realizarse **únicamente** en entornos de desarrollo / laboratorio y con cuentas creadas expresamente para la práctica. Nunca ataques sistemas de terceros.

---

<a id="indice"></a>
## Índice
1. [Objetivo](#objetivo)  
2. [Requisitos](#requisitos)  
3. [Instalación y puesta en marcha](#instalacion-y-puesta-en-marcha)  
4. [Endpoints (resumen)](#endpoints-resumen)  
5. [Usuarios de prueba incluidos](#usuarios-de-prueba-incluidos)  
6. [Ejemplos `curl` (pruebas manuales)](#ejemplos-curl-pruebas-manuales)  
7. [Ejecutar la prueba controlada de fuerza bruta (laboratorio)](#ejecutar-la-prueba-controlada-de-fuerza-bruta-laboratorio)  
8. [Mediciones y registro (qué anotar)](#mediciones-y-registro-que-anotar)  
9. [Resultados esperables y análisis](#resultados-esperables-y-analisis)  
10. [Medidas de mitigación recomendadas](#medidas-de-mitigacion-recomendadas)  
11. [Checklist de entrega](#checklist-de-entrega)  
12. [Advertencias de seguridad y ética](#advertencias-de-seguridad-y-etica)  
13. [requirements.txt](#requirementstxt)  
14. [Autor](#autor)

---

<a id="objetivo"></a>
## Objetivo
- Diseñar e implementar endpoints CRUD seguros para el recurso `Usuario`.  
- Comprender cómo un ataque de fuerza bruta puede explotar credenciales débiles.  
- Medir recursos y efectos del experimento.  
- Justificar estadísticas y proponer mitigaciones.

---

<a id="requisitos"></a>
## Requisitos
- **Python 3.8+**  
- `pip`  
- (Opcional) `jq` para formatear JSON en la terminal  
- Entorno local / máquina propia para ejecutar la API

---

<a id="instalacion-y-puesta-en-marcha"></a>
## Instalación y puesta en marcha

1. Clona el repositorio (si aplica):
git clone https://github.com/TU-USUARIO/mi-repo.git
cd mi-repo

Crea y activa un entorno virtual:
python3 -m venv venv
source venv/bin/activate    # Linux / macOS
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

Instala dependencias desde requirements.txt:
pip install -r requirements.txt

Si no tienes requirements.txt, instala manualmente:
pip install fastapi uvicorn pydantic requests python-multipart

Ejecuta la API (modo desarrollo):
uvicorn main:app --reload --host 127.0.0.1 --port 8000
API disponible en: http://127.0.0.1:8000

Swagger UI (docs): http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

<a id="endpoints-resumen"></a>

Endpoints (resumen)
Método	Ruta	Descripción	Payload / Notas
GET	/	Mensaje de salud	—
GET	/users	Listar usuarios (opcional skip, limit)	Query params
GET	/users/{id}	Obtener usuario por id	—
POST	/users/	Crear usuario	JSON {id, username, password, email?, is_active?}
PUT	/users/{id}	Actualizar usuario (no password en este ejercicio)	JSON con campos a actualizar
DELETE	/users/{id}	Eliminar usuario	—
POST	/login	Autenticación (form-data)	Form: username, password

Nota de seguridad: en este proyecto las contraseñas (por simplicidad) se guardan en texto plano en memoria solo para pruebas locales. En producción siempre hash y nunca devolver el campo password.

<a id="usuarios-de-prueba-incluidos"></a>

Usuarios de prueba incluidos
id	username	password	email
1	testuser	123	test@example.com
2	diegosantillan625@gmail.com	123456789	diegosantillan625@gmail.com
3	juanperez	abc123	test@yo.com
4	diego	abc	yo@yo.com

Usa estas cuentas solo en tu entorno de laboratorio o crea otras cuentas de prueba.

<a id="ejemplos-curl-pruebas-manuales"></a>

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
<a id="ejecutar-la-prueba-controlada-de-fuerza-bruta-laboratorio"></a>

Ejecutar la prueba controlada de fuerza bruta (laboratorio)
Reglas obligatorias:

Ejecutar solo en tu entorno local o laboratorio personal.

Usar únicamente cuentas de prueba creadas para la práctica.

Limitar el espacio de búsqueda y la velocidad (por ejemplo: digits, max_len <= 3).

Registrar métricas y resultados.

Opción A — Script Python interactivo (incluido)
Activa el entorno virtual:
source venv/bin/activate
Ejecuta:
python3 bruteforce.py
Responde a las preguntas interactivas, por ejemplo:

less
Usuario objetivo: diego
Longitud máxima (ej. 3): 3
Alfabeto (digits|alpha|all) [digits]: digits
Imprimir cada N intentos [1000]: 100
Opción B — Wrapper bash (si existe bruteforcebash.sh)
chmod +x bruteforcebash.sh
./bruteforcebash.sh
Recomendaciones durante la ejecución
Comienza con max_len = 1 o 2 para confirmar comportamiento.

Añade sleep entre intentos si el script lo permite para reducir impacto.

Supervisa el servicio y detén la prueba si observas efectos adversos.

<a id="mediciones-y-registro-que-anotar"></a>

Mediciones y registro (qué anotar)
Durante la prueba registra al menos:

Métrica	Por qué
Usuario objetivo	identificación del caso de prueba
Parámetros (alfabeto, max_len, print_every, sleep)	reproducibilidad
Hora inicio / fin	duración total
Intentos totales	coste computacional
Resultado (contraseña encontrada / no encontrada)	objetivo
Códigos HTTP (fallo / éxito)	comportamiento del servidor
Latencia media por petición	impacto en performance
Uso CPU / memoria del servidor (opcional)	efecto en recursos

Sugerencia de log CSV:

makefile
Copiar código
timestamp,attempts,username,candidate,http_code,elapsed_seconds
2025-10-03T22:15:00,120,diego,007,401,0.035
<a id="resultados-esperables-y-analisis"></a>

Resultados esperables y análisis
Contraseñas cortas y solo dígitos suelen descubrirse muy rápido.

El tiempo crece exponencialmente al aumentar longitud y/o tamaño del alfabeto.

Con medidas como rate limiting o lockouts, el éxito del ataque se reduce drásticamente.

Documenta: intentos hasta éxito, tiempo total, latencia media y cualquier bloqueo observado.

<a id="medidas-de-mitigacion-recomendadas"></a>

Medidas de mitigación recomendadas
Hash de contraseñas (bcrypt/argon2) antes de almacenar.

Política de contraseñas: longitud mínima y blacklist de contraseñas comunes.

Rate limiting por IP y por cuenta.

Lockout temporal tras N intentos fallidos.

CAPTCHA / paso adicional tras varios intentos fallidos.

Autenticación multifactor (MFA) para cuentas sensibles.

TLS/HTTPS en producción.

No revelar en errores si el usuario existe o no.

Monitorización y alertas sobre patrones de fuerza bruta.

Tests automatizados que verifiquen bloqueo y políticas.

<a id="checklist-de-entrega"></a>

Checklist de entrega
 Código de la API (main.py) y demás fuentes.

 requirements.txt.

 Scripts de prueba (bruteforce.py, bruteforcebash.sh) — solo para laboratorio.

 Logs/CSV con resultados de la prueba.

 Informe con análisis, gráficos y propuestas de mitigación.

<a id="advertencias-de-seguridad-y-etica"></a>

Advertencias de seguridad y ética
Ejecuta pruebas solo en entornos propios o con autorización explícita.

No realices ataques contra terceros.

Limita el espacio de búsqueda y la velocidad.

No uses datos o contraseñas reales durante las pruebas.

Documenta todo el experimento para replicabilidad y responsabilidad.

<a id="requirementstxt"></a>

requirements.txt
Incluye un archivo requirements.txt en la raíz del proyecto con, al menos, estas dependencias recomendadas:

makefile
Copiar código
fastapi==0.95.2
uvicorn[standard]==0.23.1
pydantic==1.10.12
requests==2.31.0
python-multipart==0.0.6
Ajusta versiones según tu entorno. Añade bcrypt/pytest/otras si las usas.

<a id="autor"></a>

Autor
Diego Ruiz
Universidad Internacional del Ecuador (UIDE)
Proyecto académico — Seguridad informática y APIs con FastAPI
Quito, Ecuador — 2025
