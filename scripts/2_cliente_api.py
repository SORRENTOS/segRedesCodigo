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
async def consultar_ia(session, payload_log):
    """
    Inyecta el log a la API de Groq sin bloquear el hilo principal.
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # PROMPT ESTRATÉGICO: Obligamos a la IA a responder como máquina (JSON)
    prompt_sistema = """
Eres un motor de triaje del SOC de Fintech Sur.
Analiza el evento de red provisto y devuelve EXCLUSIVAMENTE un objeto JSON válido.
No incluyas texto adicional, ni saludos, ni formato Markdown.
Estructura matemática requerida:
{
    "nivel_riesgo": "ALTO/MEDIO/BAJO",
    "ip_atacante": "dirección_ip_extraída",
    "accion_recomendada": "comando_iptables_o_bloqueo"
}
"""
    data = {
        "model": "llama3-8b-8192", # Modelo ultra-rápido de Groq
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Evento detectado: {payload_log}"}
        ],
        "temperature": 0.1 # Temperatura casi cero para evitar alucinaciones
    }

    inicio_tiempo = time.time()

    try:
        # Petición POST no bloqueante
        async with session.post(URL, headers=headers, json=data) as response:
            if response.status != 200:
                print(f"[ERROR API] Código HTTP: {response.status}. Revisa el Endpoint o Llave.")
                return None

            respuesta_cruda = await response.json()
            tiempo_total = round((time.time() - inicio_tiempo) * 1000, 2)
            print(f"[*] Respuesta de IA recibida en {tiempo_total} ms.")

            # Navegación del árbol JSON devuelto por Groq/OpenAI
            contenido_ia = respuesta_cruda['choices'][0]['message']['content']
            return contenido_ia

    except Exception as e:
        print(f"[ERROR SISTEMA] Falla de conexión de red: {e}")
        return None
    import json

async def main():
    # Simulamos un ataque interceptado por nuestro IDS local
    evento_falso = "Múltiples intentos fallidos de login SSH (root) desde IP 192.168.1.100 en el servidor web."

    print(f"\n[*] Analizando telemetría: '{evento_falso}'")

    async with aiohttp.ClientSession() as session:
        resultado_texto = await consultar_ia(session, evento_falso)

    if resultado_texto:
        try:
            # Convertimos la respuesta de texto plano a un Diccionario Python real
            datos_estructurados = json.loads(resultado_texto)

            print("\n--- REPORTE DE EXTRACCIÓN FINTECH SUR ---")
            print(f"Riesgo Evaluado: {datos_estructurados.get('nivel_riesgo', 'DESCONOCIDO')}")
            print(f"Objetivo Hostil: {datos_estructurados.get('ip_atacante', 'NO_ENCONTRADA')}")
            print(f"Mitigación SOC: {datos_estructurados.get('accion_recommended', 'NINGUNA')}")
            print("---------------------------------------")

        except json.JSONDecodeError:
            print("\n[CRÍTICO] La IA alucinó y no devolvió un JSON válido.")
            print(f"Respuesta cruda interceptada:\n{resultado_texto}")

if __name__ == "__main__":
    # Arrancamos el bucle de eventos asíncrono
    asyncio.run(main())