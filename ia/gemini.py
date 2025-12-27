# ia/gemini.py
from google import genai
import os
import re
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Cliente Gemini
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))


def analizar_texto(texto, max_tokens=150):
    """
    Analiza un texto como chatbot de apoyo emocional
    y devuelve un JSON válido como string.
    """

    prompt = f"""
Eres un asistente de apoyo emocional.

INSTRUCCIONES OBLIGATORIAS:
- Devuelve ÚNICAMENTE un JSON válido.
- NO escribas texto antes ni después.
- NO uses markdown.
- NO uses ``` ni explicaciones.
- Usa solo comillas dobles.

Mensaje del usuario:
"{texto}"

El JSON debe tener EXACTAMENTE esta estructura:

{{
  "mensaje_chat": "respuesta cálida, empática y natural",
  "emocion_principal": "string",
  "nivel_estres": número entre 0 y 100,
  "preocupaciones": "string",
  "recomendacion": "string"
}}
"""

    try:
        # Llamada al modelo
        response = client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=[prompt]
        )

        # Obtener texto devuelto
        if hasattr(response, "text") and response.text:
            raw_text = response.text.strip()
        elif hasattr(response, "content") and response.content:
            raw_text = response.content[0].text.strip()
        else:
            return json.dumps({
                "mensaje_chat": "No pude generar una respuesta en este momento.",
                "emocion_principal": "desconocida",
                "nivel_estres": 0,
                "preocupaciones": "",
                "recomendacion": ""
            })

        # 🔎 Extraer SOLO el JSON (por seguridad)
        match = re.search(r"\{[\s\S]*\}", raw_text)
        if not match:
            raise ValueError("No se encontró JSON en la respuesta")

        json_text = match.group()

        # Validar que sea JSON válido
        data = json.loads(json_text)

        # Devolver JSON limpio como string
        return json.dumps(data, ensure_ascii=False)

    except Exception as e:
        # Manejo de errores
        error_msg = str(e)

        if "RESOURCE_EXHAUSTED" in error_msg:
            return json.dumps({
                "mensaje_chat": "Parece que el servicio está saturado. Intenta más tarde.",
                "emocion_principal": "frustración",
                "nivel_estres": 40,
                "preocupaciones": "Servicio temporalmente no disponible",
                "recomendacion": "Intenta nuevamente en unos minutos."
            }, ensure_ascii=False)

        if "NOT_FOUND" in error_msg:
            return json.dumps({
                "mensaje_chat": "Hubo un problema técnico con el modelo de IA.",
                "emocion_principal": "confusión",
                "nivel_estres": 30,
                "preocupaciones": "Modelo no encontrado",
                "recomendacion": "Revisa la configuración del sistema."
            }, ensure_ascii=False)

        return json.dumps({
            "mensaje_chat": "Ocurrió un error inesperado al analizar el mensaje.",
            "emocion_principal": "desconocida",
            "nivel_estres": 0,
            "preocupaciones": error_msg,
            "recomendacion": "Intenta nuevamente."
        }, ensure_ascii=False)
