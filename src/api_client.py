import requests
from loguru import logger
import sys
import os

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

logger.remove()

# Logs en consola
logger.add(sys.stdout, level="INFO")

# Logs en archivo
logger.add(
    "logs/clima.log",
    rotation="1 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 4.61,
    "longitude": -74.08,
    "current_weather": True
}

def get_weather():
    logger.info("Iniciando solicitud a la API de Open-Meteo")

    try:
        response = requests.get(API_URL, params=PARAMS, timeout=5)

        if response.status_code == 200:
            data = response.json()
            logger.info("Respuesta exitosa de la API")
            return data

        elif response.status_code == 503:
            logger.warning("Servicio no disponible (503). Activando fallback.")
            return fallback_response()

        else:
            logger.error(f"Respuesta inesperada: {response.status_code}")
            return fallback_response()

    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con la API")
        return fallback_response()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {e}")
        return fallback_response()

def fallback_response():
    logger.info("Ejecutando respuesta de respaldo (fallback)")
    return {
        "source": "fallback",
        "message": "Datos no disponibles en este momento"
    }

if __name__ == "__main__":
    result = get_weather()
    print(result)
