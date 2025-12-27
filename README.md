🧠 Sistema de Bienestar Emocional Estudiantil con IA
📋 Descripción del Proyecto
Sistema web interactivo que utiliza inteligencia artificial para analizar y monitorear el bienestar emocional de estudiantes. La aplicación permite a los estudiantes expresar sus emociones y recibir análisis automatizado, mientras que los psicólogos pueden visualizar el progreso emocional de los usuarios.

🚀 Guía de Configuración Paso a Paso
PASO 1: Abrir el Proyecto
Descargue y extraiga el proyecto en su computadora

Abra la carpeta del proyecto en Visual Studio Code (o su editor preferido)

Asegúrese de estar ubicado en la carpeta raíz del proyecto

PASO 2: Crear Entorno Virtual
Ejecute el siguiente comando en la terminal:

bash
python -m venv venv
✅ Verificación: Aparecerá una carpeta llamada venv en su proyecto

PASO 3: Activar el Entorno Virtual
En la terminal, ejecute:

Para Windows:

bash
venv\Scripts\activate
Para Mac/Linux:

bash
source venv/bin/activate
✅ Verificación: Verá (venv) al inicio de la línea de comandos

PASO 4: Instalar Dependencias
Copie y pegue TODO este bloque en la terminal:

bash
pip install streamlit
pip install google-genai
pip install google-generativeai
pip install matplotlib
pip install pandas
pip install nltk
pip install python-dotenv
✅ Verificación: Todas las librerías se instalarán sin errores

PASO 5: Configurar la Clave API de Google AI
En la carpeta raíz del proyecto, cree un archivo llamado .env

Abra el archivo .env y pegue su clave API:

env
GENAI_API_KEY=su_clave_api_aqui
🔑 Obtener clave API: Visite Google AI Studio

PASO 6: Ejecutar la Aplicación
En la terminal (con el entorno virtual activado), ejecute:

bash
streamlit run app.py
✅ Éxito: La aplicación se abrirá automáticamente en:
👉 http://localhost:8501

