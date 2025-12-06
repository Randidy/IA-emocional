# ia/gemini.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def analizar_texto(texto):
    prompt = f"""
Responde como una persona real que está escuchando a alguien que necesita apoyo emocional.
Habla con naturalidad, empatía y variedad. Nada robótico.

Mensaje del usuario:
'{texto}'

Incluye también un pequeño análisis emocional:
- emoción_principal
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
        # Modelo correcto y compatible con tu API
        response = client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=[prompt]
        )

        # Obtener texto (forma segura)
        if hasattr(response, "text") and response.text:
            return response.text.strip()

        if hasattr(response, "content") and response.content:
            return response.content[0].text.strip()

        return "Error: respuesta vacía del modelo."

    except Exception as e:
        return f"Error procesando análisis: {e}"
