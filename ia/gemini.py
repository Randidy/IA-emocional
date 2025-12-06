# ia/gemini.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def analizar_texto(texto):
    prompt = f"""
Analiza este texto emocional:
'{texto}'
Devuélveme:
- emoción principal
- nivel de estrés (0 al 100)
- preocupaciones
- recomendación breve para el estudiante
"""

    # Llamada a Gemini API
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=[prompt]  # lista de strings
    )

    # Forma correcta de obtener el texto
    if hasattr(response, "text"):
        return response.text.strip()
    elif hasattr(response, "content"):
        return response.content[0].text.strip()
    else:
        return str(response)
