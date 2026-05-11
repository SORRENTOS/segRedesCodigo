# =====================================================================
# ARCHIVO: motor_firewall.py (Módulo de Respuesta Activa)
# =====================================================================
import subprocess
import shlex

def aislar_atacante(ip_objetivo):
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
    comando_iptables = ["sudo", "iptables", "-A", "INPUT", "-s", ip_objetivo, "-j", "DROP"]

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
    aislar_atacante("192.168.1.50")
    
    # Prueba 2: Un intento de Inyección de Comandos
    # Gracias al Hito 1, esto NO ejecutará el comando 'rm -rf'
    aislar_atacante("8.8.8.8; rm -rf /")