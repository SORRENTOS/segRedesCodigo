import asyncio 
import aiohttp 
import json 
import time
import re  # HITO: Necesario para capturar la IP real [cite: 10]
from motor_firewall import aislar_atacante # HITO 1: Integración de respuesta activa [cite: 3]

# =====================================================================
# HITO 1: IMPORTACIONES CORPORATIVAS FINTECH SUR
# =====================================================================
from motor_dlp import ofuscar_datos 
from cliente_api import consultar_ia 

# =====================================================================
# HITO 2: EL BUCLE ASÍNCRONO CENTRAL
# =====================================================================
async def pipeline_defensivo(evento_crudo): 
    """
    Cadena de montaje estricta: Ingesta -> DLP -> IA -> Respuesta Activa
    """
    print("=====================================================")
    print(f"[*] 1. ALERTA RECIBIDA (IDS): \n    '{evento_crudo}'") 
    print("=====================================================")

    # ---------------------------------------------------------------------
    # HITO 2.5: CAPTURA TÁCTICA DE LA IP (Visión Táctica)
    # Extraemos la IP real ANTES de que el DLP la censure 
    # ---------------------------------------------------------------------
# ---------------------------------------------------------------------
    # HITO 2.5: CAPTURA TÁCTICA DE LA IP (Visión Táctica)

    ip_real_match = re.search(r"hostil\s+((?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}|(?:[a-fA-F0-9]{1,4}:){1,7}[a-fA-F0-9]{1,4}|::))", evento_crudo)
    

    ip_hostil_real = ip_real_match.group(1) if ip_real_match else "NO_ENCONTRADA"

    if ip_hostil_real != "NO_ENCONTRADA":
        print(f" [+] IP Real capturada y retenida en memoria: {ip_hostil_real} ")

    # =====================================================================
    # HITO 3: ESCUDO LEGAL (DLP) - LEY 21.719 
    # =====================================================================
    print("\n[*] 2. Iniciando motor de ofuscación (Ley 21.719)...") 
    inicio_dlp = time.time() 
    
    # Se sanitiza el log. La IA nunca verá los datos sensibles 
    evento_seguro = ofuscar_datos(evento_crudo) 
    
    if "[ERROR]" in evento_seguro:
        print("[-] [CRÍTICO] Pipeline abortado por falla estructural en el DLP.")
        return 
        
    tiempo_dlp = round((time.time() - inicio_dlp) * 1000, 2)
    print(f"[+] Sanitización completada en {tiempo_dlp} ms. ") 
    print(f"    Payload Seguro: '{evento_seguro}'") 

    # =====================================================================
    # HITO 4: CEREBRO IA (Conexión Asíncrona)
    # =====================================================================
    print("\n[*] 3. Transmitiendo telemetría limpia al LLM...")
    
    async with aiohttp.ClientSession() as session:
        # Enviamos el evento ofuscado para cumplir la norma 
        resultado_ia_texto = await consultar_ia(session, evento_seguro)

    # =====================================================================
    # HITO 5: EXTRACCIÓN Y RESPUESTA ACTIVA (ISO 42001)
    # =====================================================================
    if resultado_ia_texto: 
        try:
            datos = json.loads(resultado_ia_texto) 
            nivel_riesgo = datos.get('nivel_riesgo', 'DESCONOCIDO').upper() 

            print("\n=====================================================")
            print("         REPORTE DE EXTRACCIÓN FINTECH SUR           ")
            print("=====================================================")
            print(f" RIESGO:      {nivel_riesgo}") 
            print(f" IP DETECTADA: {datos.get('ip_atacante', 'NO ENCONTRADA')}") 
            print(f" MITIGACIÓN:  {datos.get('accion_recomendada', 'NINGUNA')}") 
            print("=====================================================\n")

            # ACTIVACIÓN DE DEFENSA AUTOMÁTICA [cite: 10]
            print(ip_hostil_real)
            if nivel_riesgo in ["ALTO", "CRITICO"] and ip_hostil_real != "NO_ENCONTRADA":
                print(f"[*] 4. ACTIVADO. Transfiriendo IP REAL {ip_hostil_real} al Motor de Firewall...")
                # Llamada al módulo del Lab 7
                aislar_atacante(ip_hostil_real) 
            else:
                print("[*] 4. Sin parámetros críticos o sin IP válida. No se requiere acción.")
            
        except json.JSONDecodeError: 
            print("\n[CRÍTICO] La IA alucinó y no devolvió un JSON válido.") 
    else:
        print("\n[-] [CRÍTICO] Falla de comunicación con la API.") 

# =====================================================================
# GATILLO DE EJECUCIÓN
# =====================================================================
if __name__ == "__main__": 
    print("Seleccione el tipo de prueba: \n 1) Simulación por defecto \n 2) RUT e IP personalizados")
    opcion = input()
    
    payload_simulado = (
  "[ALERTA IDS] Ataque en cadena detectado. Proxy legítimo 10.0.0.2 reenvió tráfico "
    "desde IP hostil 185.10.20.30 hacia servidor crítico 192.168.1.1. "
    "RUT del administrador del proxy: 11.111.111-1"
    )

    if opcion == "2":
        rut = input("Indique un RUT: ")
        ip = input("Indique una IP atacante: ")
        ip2 = input("Indique IP del dispositivo atacado: ")
        if rut and ip and ip2:
            payload_simulado = f"Ataque detectado desde {ip} hacia {ip2} con RUT {rut}."

    print("\n[*] Iniciando Orquestador SOC Fintech Sur...\n") 
    asyncio.run(pipeline_defensivo(payload_simulado))