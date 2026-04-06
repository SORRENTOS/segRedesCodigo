import time
import sys

try:
    # Intenta importar el motor DLP del estudiante
    from motor_dlp import ofuscar_datos
except ImportError:
    print("[-] [ERROR CRÍTICO] No se encontró el archivo 'motor_dlp.py' o la función 'ofuscar_datos'.")
    sys.exit(1)

def ejecutar_auditoria():
    print("=========================================================")
    print("      🛡️ INICIANDO AUDITORÍA CISO - FINTECH SUR 🛡️")
    print("=========================================================\n")
    
    fallos = 0
    
    # BATERÍA DE PRUEBAS BASADA EN MATRIZ DE RIESGOS
    casos_prueba = [
        {
            "id": "1",
            "riesgo": "Falso Positivo IPv4 (>255)",
            "entrada": "IP inválida: 999.999.999.999",
            "esperado": "IP inválida: 999.999.999.999" # No debe ofuscarse
        },
        {
            "id": "2",
            "riesgo": "Desbordamiento de dígitos",
            "entrada": "Número largo: 12345.678.910.1112",
            "esperado": "Número largo: 12345.678.910.1112" # No debe ofuscarse
        },
        {
            "id": "3",
            "riesgo": "Ausencia de límite de palabra",
            "entrada": "IP dentro de número: 192.168.1.1000",
            "esperado": "IP dentro de número: 192.168.1.1000" # El 1000 invalida la IP
        },
        {
            "id": "4",
            "riesgo": "RUT Nulo / Mal formado",
            "entrada": "RUT nulo: 00.000.000-0",
            "esperado": "RUT nulo: 00.000.000-0" # Depende de política, asumimos estricta (no ofuscar si es inválido matemáticamente)
        },
        {
            "id": "5",
            "riesgo": "RUT con dígito incorrecto",
            "entrada": "RUT inválido: 12345678-0",
            "esperado": "RUT inválido: 12345678-0" # El dígito real de 12345678 es K.
        }
    ]

    print("[*] FASE 1: AUDITORÍA DE EXPRESIONES REGULARES (EDGE CASES)")
    for caso in casos_prueba:
        resultado = ofuscar_datos(caso["entrada"])
        
        if resultado == caso["esperado"]:
            print(f"  [+] Caso {caso['id']} APROBADO: {caso['riesgo']}")
        else:
            print(f"  [-] Caso {caso['id']} REPROBADO: {caso['riesgo']}")
            print(f"      - Entrada  : {caso['entrada']}")
            print(f"      - Tu salida: {resultado}")
            fallos += 1

    print("\n[*] FASE 2: AUDITORÍA DE RESILIENCIA DE TIPOS (MANEJO DE EXCEPCIONES)")
    try:
        # Prueba de entrada no string (Ej. un número entero o None)
        ofuscar_datos(12345)
        print("  [+] APROBADO: El motor manejó correctamente una entrada no-string (TypeError mitigado).")
    except Exception as e:
        print(f"  [-] REPROBADO: El motor colapsó al recibir un entero en lugar de un string. Error: {type(e).__name__}")
        fallos += 1

    print("\n[*] FASE 3: AUDITORÍA DE RENDIMIENTO (BENCHMARKING)")
    texto_carga = "Ataque desde 192.168.1.50 hacia el servidor con RUT 18.123.456-7. " * 50
    inicio_tiempo = time.time()
    
    # Bucle de 10,000 llamadas para medir recompilación de Regex
    try:
        for _ in range(10000):
            ofuscar_datos(texto_carga)
        tiempo_total = time.time() - inicio_tiempo
        print(f"  [+] APROBADO: 10,000 iteraciones procesadas en {tiempo_total:.4f} segundos.")
        if tiempo_total > 2.0:
            print("  [!] ADVERTENCIA DE RENDIMIENTO: Tu código es lento. ¿Estás recompilando la Regex en cada llamada en lugar de usar re.compile() globalmente?")
    except Exception as e:
        print("  [-] REPROBADO: El motor falló durante la prueba de estrés.")
        fallos += 1

    print("\n=========================================================")
    if fallos == 0:
        print("🟢 DICTAMEN: CERTIFICACIÓN DLP APROBADA. LISTO PARA PRODUCCIÓN.")
    else:
        print(f"🔴 DICTAMEN: REPROBADO. Se detectaron {fallos} vulnerabilidades estructurales.")
        print("             Refactorice su código en 'motor_dlp.py' y vuelva a intentarlo.")
    print("=========================================================")

if __name__ == "__main__":
    ejecutar_auditoria()