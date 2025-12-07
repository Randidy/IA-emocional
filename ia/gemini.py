# ia/gemini.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def analizar_texto(texto, max_tokens=150):
    """
    Analiza el texto como un chatbot de apoyo emocional.
    Se indica dentro del prompt para limitar la longitud de la respuesta.
    """
    prompt = f"""
Responde como una persona real que está escuchando a alguien que necesita apoyo emocional.
Habla con naturalidad, empatía y variedad. Nada robótico.
Limita tu respuesta a aproximadamente {max_tokens} tokens.

Mensaje del usuario:
'{texto}'

Incluye también un pequeño análisis emocional:
- emocion_principal
- nivel_estres (0 a 100)
- preocupaciones
- recomendacion

Devuelve TODO en formato JSON:
{{
  "mensaje_chat": "respuesta cálida y natural",
  "emocion_principal": "string",
  "nivel_estres": numero,
  "preocupaciones": "string",
  "recomendacion": "string"
}}
"""

    try:
        # Llamada al modelo (sin max_output_tokens, solo control por prompt)
        response = client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=[prompt]
        )

        # Obtener el texto de forma segura
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if hasattr(response, "content") and response.content:
            return response.content[0].text.strip()

        return "Error: respuesta vacía del modelo."

    except Exception as e:
        error_msg = str(e)
        if "RESOURCE_EXHAUSTED" in error_msg:
            return "Error: cuota agotada. Espera o usa otra clave."
        if "NOT_FOUND" in error_msg:
            return "Error: modelo no disponible. Revisa nombre del modelo."
        return f"Error procesando análisis: {e}"
