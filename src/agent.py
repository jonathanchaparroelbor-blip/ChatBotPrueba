import os
from loguru import logger
from dotenv import load_dotenv
import requests

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("AI_API_KEY")
API_URL = os.getenv("AI_API_URL")

def generate_response(user_input: str) -> str:
    if not API_KEY or not API_URL:
        logger.error("Credenciales de IA no configuradas")
        return "Error interno del sistema."

    payload = {
        "prompt": user_input,
        "max_tokens": 100
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        logger.info("Enviando solicitud a la API de IA")
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            logger.success("Respuesta generada correctamente")
            return response.json().get("response", "Respuesta vacía")

        elif response.status_code >= 500:
            logger.error("Falla del servidor de IA")
            return fallback_response(user_input)

        else:
            logger.warning(f"Respuesta inesperada: {response.status_code}")
            return fallback_response(user_input)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con la IA: {e}")
        return fallback_response(user_input)

def fallback_response(user_input: str) -> str:
    logger.info("Ejecutando fallback")
    return "En este momento no puedo procesar tu solicitud, por favor intenta más tarde."

if __name__ == "__main__":
    logger.add("logs/agent.log", rotation="1 MB")

    user_text = input("Usuario: ")
    answer = generate_response(user_text)

    print("Agente:", answer)
