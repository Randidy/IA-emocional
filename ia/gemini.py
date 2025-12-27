from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def analizar_texto(texto):
    prompt = f"""
Responde como una persona real que brinda apoyo emocional.
Habla con empatía, cercanía y naturalidad.

Mensaje del usuario:
"{texto}"

Devuelve SOLO JSON:
{{
  "mensaje_chat": "respuesta empática",
  "emocion_principal": "string",
  "nivel_estres": numero,
  "preocupaciones": "string",
  "recomendacion": "string"
}}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=[prompt]
    )

    return response.text.strip()
