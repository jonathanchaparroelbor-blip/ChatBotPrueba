from loguru import logger
import requests

SERVICE_URL = "http://httpbin.org/status/200"

def check_service():
    try:
        logger.info("Iniciando verificación del servicio...")
        response = requests.get(SERVICE_URL, timeout=5)

        if response.status_code == 200:
            logger.success("Servicio activo (200 OK)")
        elif response.status_code >= 500:
            logger.error(f"Falla del servidor: {response.status_code}")
        else:
            logger.warning(f"Estado inesperado: {response.status_code}")

    except requests.exceptions.Timeout:
        logger.error("Timeout: el servicio no respondió a tiempo")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    logger.add("logs/service.log", rotation="1 MB")
    check_service()
