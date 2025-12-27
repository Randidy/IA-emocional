# 🧠 Sistema de Bienestar Emocional Estudiantil con IA

> **Proyecto de soporte emocional y monitoreo psicológico mediante Inteligencia Artificial.**

---

## 🚀 GUÍA DE EJECUCIÓN PASO A PASO (Windows)

Siga estos pasos estrictamente para ejecutar el proyecto en su computadora.

### 📂 PASO 1: Abrir el Proyecto
Descargue el proyecto, descomprímalo y abra la carpeta en **Visual Studio Code** (o su terminal favorita). Asegúrese de estar ubicado en la carpeta raíz.

### 🐍 PASO 2: Crear Entorno Virtual
Escriba el siguiente comando en la terminal para crear un espacio aislado para el proyecto:

```bash
python -m venv venv

⚡ PASO 3: Activar el Entorno
Es fundamental activar el entorno antes de instalar nada. Ejecute:

venv\Scripts\activate

✅ Verificación: Debería ver (venv) al principio de su línea de comandos.

📦 PASO 4: Instalar Dependencias
Copie y pegue los siguientes comandos para instalar las librerías una por una:

pip install streamlit
pip install google-genai
pip install google-generativeai
pip install matplotlib
pip install pandas
pip install nltk
pip install python-dotenv

🔑 PASO 5: Configurar la Clave API
El sistema necesita la clave de Google para funcionar.

Cree un archivo nuevo llamado .env en la carpeta raíz.

Pegue su clave dentro del archivo así:

GENAI_API_KEY=su_clave_api_aqui

▶️ PASO 6: Ejecutar la Aplicación
Finalmente, inicie el sistema con este comando:

streamlit run app.py

📋 Descripción del Sistema
Estudiante: Chatbot con IA para contención emocional y registro de bitácora.

Psicólogo: Panel administrativo para ver el historial y alertas de estrés.

Tecnologías: Python, Streamlit, Google Gemini AI, SQLite.
