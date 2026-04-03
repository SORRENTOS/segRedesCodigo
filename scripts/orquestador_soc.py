import asyncio 
import aiohttp 
import json 
import time 

# =====================================================================
# HITO 1: IMPORTACIONES CORPORATIVAS FINTECH SUR [cite: 4, 5, 24]
# =====================================================================
# Se importan las funciones desde los archivos renombrados sin números 
from motor_dlp import ofuscar_datos 
from cliente_api import consultar_ia 

# =====================================================================
# HITO 2: EL BUCLE ASÍNCRONO CENTRAL [cite: 7, 8]
# =====================================================================
async def pipeline_defensivo(evento_crudo): 
    """
    Cadena de montaje estricta: Ingesta -> DLP -> IA -> Extracción
    """
    # Se imprime el log original apenas ingresa al sistema 
    print("=====================================================")
    print(f"[*] 1. ALERTA RECIBIDA (IDS): \n    '{evento_crudo}'") 
    print("=====================================================")

    # =====================================================================
    # HITO 3: ESCUDO LEGAL (DLP) - LEY 21.719 
    # =====================================================================
    print("\n[*] 2. Iniciando motor de ofuscación (Ley 21.719)...") 
    inicio_dlp = time.time() 
    
    # Se llama al motor DLP para sanitizar el log [cite: 11, 26]
    # REGLA DE NEGOCIO: A partir de aquí no se usa más 'evento_crudo' [cite: 13]
    evento_seguro = ofuscar_datos(evento_crudo) 
    
    # Bloque Fail-Fast para asegurar la integridad estructural [cite: 27]
    if "[ERROR]" in evento_seguro:
        print("[-] [CRÍTICO] Pipeline abortado por falla estructural en el DLP.")
        return 
        
    tiempo_dlp = round((time.time() - inicio_dlp) * 1000, 2)
    print(f"[+] Sanitización completada en {tiempo_dlp} ms.") 
    print(f"    Payload Seguro: '{evento_seguro}'") 

    # =====================================================================
    # HITO 4: CEREBRO IA (Conexión Asíncrona) [cite: 14, 28]
    # =====================================================================
    print("\n[*] 3. Transmitiendo telemetría limpia al LLM...")
    
    # Se abre la sesión asíncrona para consumir la API [cite: 15, 28]
    async with aiohttp.ClientSession() as session:
        # Se envía el evento seguro (sanitizado) a la IA 
        resultado_ia_texto = await consultar_ia(session, evento_seguro)

    # =====================================================================
    # HITO 5: EXTRACCIÓN Y TRIAJE (Parseo de JSON) [cite: 17, 31]
    # =====================================================================
    if resultado_ia_texto: 
        try:
            # Conversión del texto JSON en diccionario de Python [cite: 18, 31]
            datos = json.loads(resultado_ia_texto)
            
            # Impresión del Reporte Ejecutivo con las claves extraídas [cite: 19, 31]
            print("\n=====================================================")
            print("         REPORTE DE EXTRACCIÓN FINTECH SUR           ")
            print("=====================================================")
            print(f" RIESGO:      {datos.get('nivel_riesgo', 'DESCONOCIDO')}") 
            print(f" IP ATACANTE: {datos.get('ip_atacante', 'NO ENCONTRADA')}") 
            print(f" MITIGACIÓN:  {datos.get('accion_recomendada', 'NINGUNA')}") 
            print("=====================================================\n")
            
        except json.JSONDecodeError: 
            # Manejo de errores si la IA no devuelve un JSON válido [cite: 20, 32]
            print("\n[CRÍTICO] La IA alucinó y no devolvió un JSON válido.") 
            print(f"Respuesta cruda interceptada:\n{resultado_ia_texto}") 
    else:
        print("\n[-] [CRÍTICO] Falla de comunicación con la API. Red local en riesgo.") 


# =====================================================================
# HITO 6: GATILLO DE EJECUCIÓN (Prueba End-to-End) [cite: 21, 32]
# =====================================================================
if __name__ == "__main__": 
    # Payload de prueba con IP real y RUT para verificar DLP [cite: 22, 33]
    payload_simulado = (
        "Alerta 404: Múltiples ataques de fuerza bruta detectados desde la IP 192.168.1.100 "
        "y tráfico anómalo desde 10.0.0.5 hacia el usuario administrador con RUT 18.123.456-K "
        "en el puerto 22."
    )
    
    print("[*] Iniciando Orquestador SOC Fintech Sur...\n") 
    
    # Se dispara el bucle de eventos asíncrono con el log de prueba [cite: 22, 33]
    asyncio.run(pipeline_defensivo(payload_simulado))