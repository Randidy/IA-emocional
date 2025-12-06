from google import genai
import os
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

# Crear cliente con tu API Key
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

try:
    # Listar los modelos disponibles para probar la API
    response = client.models.list()
    print("✅ API funciona, modelos disponibles:", [m.name for m in response])
except Exception as e:
    print("❌ Error con la API Key:", e)
