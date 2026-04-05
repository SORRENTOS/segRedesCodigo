import pytest
import asyncio
from orquestador_soc import pipeline_defensivo 

# Definimos una lista de diferentes ataques para probar la robustez
ataques_simulados = [
    ("Fuerza bruta", "Login fallido desde IP 192.168.1.100 con RUT 12.345.678-9"),
    ("Inyección SQL", "Intento de bypass en login con 'OR 1=1' desde 10.0.0.5"),
    ("Escaneo de puertos", "Nmap detectado desde IP 172.16.0.20 hacia el puerto 80"),
    ("Acceso indebido", "Usuario 'admin' intentó acceder desde Rusia (IP 95.161.22.1)"),
    ("Dato sensible expuesto", "Log con RUT 19.876.543-2 detectado en texto plano")
]

@pytest.mark.asyncio
@pytest.mark.parametrize("tipo_ataque, payload", ataques_simulados)
async def test_pipeline_multiples_escenarios(tipo_ataque, payload):
    """
    Este test correrá 5 veces automáticamente, 
    una por cada ataque de la lista.
    """
    print(f"\n[PROBANDO ESCENARIO: {tipo_ataque}]")
    try:
        await pipeline_defensivo(payload)
        assert True
    except Exception as e:
        pytest.fail(f"El SOC falló al procesar {tipo_ataque}: {e}")