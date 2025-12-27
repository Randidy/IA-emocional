🧠 Sistema de Bienestar Emocional Estudiantil con IA
Aplicación web desarrollada en Python y Streamlit que utiliza Inteligencia Artificial Generativa (Google Gemini) para brindar soporte emocional primario a estudiantes y herramientas de monitoreo para psicólogos.

📋 Descripción del Proyecto
El sistema permite:

Rol Estudiante: Interactuar con un chatbot empático que analiza emociones, niveles de estrés y brinda recomendaciones personalizadas.

Rol Psicólogo: Visualizar un historial detallado de las interacciones de los estudiantes para una atención temprana.

Tecnología: Uso de la API google-genai para el procesamiento de lenguaje natural y SQLite para la persistencia de datos.

🛠️ Requisitos Previos
Python 3.10 o superior.

Una API Key de Google Gemini (AI Studio).

🚀 Guía de Instalación y Ejecución
Sigue estos pasos estrictamente para poner en marcha el proyecto en tu entorno local.

1. Preparar el Entorno Virtual
Abre tu terminal (consola) en la carpeta raíz del proyecto y ejecuta:

Bash

# Crear el entorno virtual
python -m venv venv
Activar el entorno virtual:

En Windows:

Bash

venv\Scripts\activate
En macOS/Linux:

Bash

source venv/bin/activate
2. Instalar Dependencias
Con el entorno activado (verás (venv) en tu terminal), ejecuta los siguientes comandos para instalar las librerías necesarias:

Bash

pip install streamlit
pip install google-genai
pip install python-dotenv
pip install matplotlib
pip install pandas
pip install nltk
Nota: Se ha incluido python-dotenv que es esencial para la seguridad de las credenciales, además de las librerías de análisis de datos solicitadas.

3. Configuración de la API Key
El sistema requiere una clave de seguridad para funcionar.

Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que app.py).

Abre el archivo y pega tu clave de Google Gemini de la siguiente manera:

Fragmento de código

GENAI_API_KEY=tu_clave_api_aqui_sin_comillas
4. Ejecución del Proyecto
Para iniciar la aplicación web, ejecuta:

Bash

streamlit run app.py
El navegador se abrirá automáticamente en http://localhost:8501.

🧪 Verificación de API (Opcional)
Si deseas verificar que tu clave de API funciona correctamente antes de abrir la aplicación web, puedes ejecutar el script de prueba incluido:

Bash

python test_api.py
Si la configuración es correcta, verás un mensaje: "✅ API funciona, modelos disponibles..."

📂 Estructura del Proyecto
app.py: Punto de entrada principal de la aplicación (Interfaz Streamlit).

database/database.py: Lógica de conexión y consultas a SQLite.

ia/gemini.py: Módulo de integración con la Inteligencia Artificial.

data/: Carpeta donde se genera automáticamente la base de datos emotional.db.

.env: Archivo de configuración de variables de entorno (No incluido en el repositorio por seguridad).

👤 Usuarios y Roles
Para probar el sistema:

Estudiante: Ingresa cualquier Nombre, Apellido y un Email válido (ej: alumno@correo.com). Selecciona el rol "Estudiante".

Psicólogo: Ingresa tus datos y selecciona el rol "Psicólogo" para ver el panel de control y el historial de los alumnos.

Proyecto desarrollado para el Curso de Pruebas de Software - 2025.
