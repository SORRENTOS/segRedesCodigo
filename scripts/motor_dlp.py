import re

def ofuscar_datos(log_crudo):
    """
    MOTOR DLP FINTECH SUR - CUMPLIMIENTO LEY 21.719
    Este módulo intercepta telemetría y censura PII antes de enviarla a la IA.
    """
    
    # 1. EL RETO REGEX 1: Direcciones IP (IPv4)
    # Los alumnos deben investigar o deducir la sintaxis exacta.
    # Pista: \b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b
    patron_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    patron_rut = r"\b\d{1,2}(?:\.\d{3}){2}-[0-9Kk]\b|\b\d{7,8}-[0-9Kk]\b"

    # 3. Aplicación de censura (Reemplazo)
    log_seguro = log_crudo
    
    # Validamos que no explote si el alumno puso mal la regex
    try:
        log_seguro = re.sub(patron_ip, "[IP_CENSURADA]", log_seguro)
        log_seguro = re.sub(patron_rut, "[RUT_CENSURADO]", log_seguro)
    except re.error as e:
        print(f"[ERROR DLP] Sintaxis Regex Inválida: {e}")
        # FAIL-SAFE: Si el DLP falla, borramos todo el log por seguridad.
        return "[ERROR] LOG DESTRUIDO POR FALLA DE DLP"

    return log_seguro

if __name__ == "__main__":
    # --- ENTORNO DE PRUEBAS (UNIT TESTING LOCAL) ---
    print("[*] Iniciando Pruebas de Motor DLP...")
    
    bateria_pruebas = [
        "Ataque de fuerza bruta desde IP 203.0.113.45 contra el servidor.",
        "El usuario con RUT 18.123.456-7 intentó acceder a base de datos.",
        "Transferencia anómala hacia 8.8.8.8 iniciada por RUT 9876543-K."
    ]
    
    for i, prueba in enumerate(bateria_pruebas, 1):
        print(f"\n--- Caso de Prueba {i} ---")
        print(f"Original : {prueba}")
        resultado = ofuscar_datos(prueba)
        print(f"Ofuscado : {resultado}")
        
        # Auditoría automática simple
        if "203.0.113.45" in resultado or "18.123.456-7" in resultado:
            print("[ALERTA LEGAL] Fuga de datos detectada. DLP Fallido.")
        else:
            print("[OK] Datos sensibles ofuscados correctamente.")