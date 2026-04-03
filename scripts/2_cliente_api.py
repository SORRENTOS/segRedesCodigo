import aiohttp
import asyncio
import os
from dotenv import load_dotenv

# 1. Cargar la bóveda de secretos corporativos
print("[*] Iniciando secuencia de arranque SOC...")
load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
URL = os.getenv("LLM_API_URL")

# 2. Validación de seguridad estricta (Fail-Fast)
if not API_KEY:
    raise ValueError("[CRÍTICO] API Key no encontrada. Revisa tu archivo .env")

if not URL:
    raise ValueError("[CRÍTICO] URL del LLM no encontrada. Revisa tu archivo .env")

# 3. Auditoría de variables en memoria (Enmascarando el secreto)
# Esto muestra los primeros 4 y últimos 4 caracteres para verificar que cargó bien sin exponerla
llave_enmascarada = f"{API_KEY[:4]}...[CENSURADO]...{API_KEY[-4:]}"

print(f"[✔] Credenciales cargadas exitosamente.")
print(f"    - Llave API: {llave_enmascarada}")
print(f"    - Endpoint: {URL}")

# Aquí continuaría tu lógica asíncrona para el motor DLP...