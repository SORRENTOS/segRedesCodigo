# =====================================================================
# ARCHIVO: motor_firewall.py (Módulo de Respuesta Activa)
# =====================================================================
import subprocess
import shlex

def aislar_atacante(ip_objetivo):
    
    # === HITO 0: ESCUDO ANTI-SUICIDIO (ISO 42001) ===
    try:
        with open("whitelist.txt", "r") as archivo_blanco:
            # Leemos las IPs ignorando comentarios y espacios [cite: 46, 47]
            ips_protegidas = [linea.strip() for linea in archivo_blanco if linea.strip() and not linea.startswith("#")]
            
            if ip_objetivo in ips_protegidas:
                print(f" [!] [ALERTA ISO 42001] La IP {ip_objetivo} es INFRAESTRUCTURA CRÍTICA.") 
                print(" [!] Operación abortada por Guardrail. Desobedeciendo a la IA.") 
                return # Salva el servidor terminando la función [cite: 51]
    except FileNotFoundError:
        print(" [-] [ADVERTENCIA] Archivo whitelist.txt no encontrado. Operando a ciegas.") 
    """
    Recibe una IP y construye el subproceso para bloquearla en iptables.
    Aplica Zero Trust: Inmunidad contra Inyección de Comandos.
    """
    print(f"\n[*] Iniciando protocolo de contención para IP: {ip_objetivo}")

    # =====================================================================
    # HITO 1: CONSTRUCCIÓN SEGURA DEL COMANDO (Vía Listas)
    # =====================================================================
    # Se utiliza una lista para evitar ataques de inyección de comandos.
    # El comando final será: sudo iptables -A INPUT -s [IP] -j DROP
    comando_base = "ip6tables" if ":" in ip_objetivo else "iptables"
    

    comando_iptables = ["sudo", comando_base, "-A", "INPUT", "-s", ip_objetivo, "-j", "DROP"]

    # AUDITORÍA VISUAL: Mostramos cómo el OS interpretará la orden
    comando_seguro_texto = shlex.join(comando_iptables)
    print(f"    [AUDITORÍA] Comando ensamblado: {comando_seguro_texto}")

    # =====================================================================
    # HITO 2: INVOCACIÓN DEL KERNEL DE LINUX
    # =====================================================================
    try:
        print("    [*] Transmitiendo orden al Firewall (Subproceso)...")
        
        # Ejecución segura mediante subprocess.run
        # shell=False (por defecto) garantiza que no se ejecute un intérprete de comandos intermedio
        resultado = subprocess.run(
            comando_iptables, 
            capture_output=True, 
            text=True
        )
        
        # Se imprime el returncode: 0 significa éxito, cualquier otro es error
        print(f"    [RESULTADO] Código de retorno del sistema: {resultado.returncode}")
        
        if resultado.returncode == 0:
            print(f"    [+] IP {ip_objetivo} bloqueada exitosamente.")
        else:
            # Es normal que devuelva error si no se tiene sudo real o la IP es inválida
            print(f"    [-] El comando falló.")
            if resultado.stderr:
                print(f"    [DETALLE] {resultado.stderr.strip()}")

    except FileNotFoundError:
        print("    [-] [ERROR] Comando 'iptables' no encontrado en este sistema operativo.")
    except Exception as e:
        print(f"    [-] [ERROR CRÍTICO] Fallo en la invocación del sistema: {e}")

# =====================================================================
# GATILLO DE PRUEBA LOCAL (Simulacro)
# =====================================================================
if __name__ == "__main__":
    print("=====================================================")
    print("      SIMULACRO DE RESPUESTA ACTIVA (DRY RUN)        ")
    print("=====================================================")
    
    # Prueba 1: Una IP legítima
    aislar_atacante("192.168.1.1")
    #ip no legitima
    aislar_atacante("200.5.123.10")    
  
    aislar_atacante("8.8.8.8; rm -rf /")