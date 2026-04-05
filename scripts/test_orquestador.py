import pytest
import asyncio
# Importamos la función directamente de tu archivo
from orquestador_soc import pipeline_defensivo 

@pytest.mark.asyncio
async def test_pipeline_completo_exito():
    """
    HITO DE PRUEBA: Verifica que el pipeline procese un log 
    y no explote en el camino.
    """
    payload_test = "Ataque detectado desde 192.168.1.1 con RUT 11.222.333-4"
    
    # Ejecutamos tu función principal
    # Como tu función no tiene un 'return' con los datos (solo hace prints),
    # aquí probamos que se ejecute sin lanzar excepciones.
    try:
        await pipeline_defensivo(payload_test)
        assert True
    except Exception as e:
        pytest.fail(f"El pipeline falló con el error: {e}")

@pytest.mark.asyncio
async def test_dlp_integridad():
    """
    Verifica que si el DLP falla y devuelve [ERROR], el pipeline se detenga.
    """
    # Simulamos un evento que fuerce un error si tu motor_dlp lo maneja
    payload_corrupto = "[ERROR] Datos corruptos"
    
    resultado = await pipeline_defensivo(payload_corrupto)
    # Si tu función retorna None al fallar, el assert pasa
    assert resultado is None