import streamlit as st
import json
import re
from ia.gemini import analizar_texto
from database.database import (
    crear_tablas,
    registrar_usuario,
    buscar_usuario,
    guardar_entrada,
    obtener_entradas
)

# Crear las tablas al iniciar
crear_tablas()

# -------------------------
# SESSION
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------
# VALIDACIONES
# -------------------------
def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_password(password):
    return len(password) >= 6


def validar_nombre(nombre):
    return len(nombre.strip()) > 0 and nombre.replace(" ", "").isalpha()


# -------------------------
# CONFIGURACIÓN
# -------------------------
st.set_page_config(
    page_title="Bienestar Emocional",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# -------------------------
# ESTILOS CSS SIMPLES
# -------------------------
def aplicar_estilos():
    st.markdown("""
    <style>
    * {
        color: #4C585B;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f4f7;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding: 0 15px;
    }

    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    .block-container {
        max-width: 500px;
        width: 100%;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .stButton > button {
        background-color: #4C8BFF;
        color: white;
        padding: 12px;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-size: 16px;
        margin-top: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #3975D1;
    }

    .stAlert {
        background-color: #FFEB3B;
        color: #444;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
    }

    h1, h3 {
        color: #4C8BFF;
        text-align: center;
    }

    .stTextInput, .stSelectbox {
        width: 100%;
        margin-bottom: 12px;
    }

    .stTextArea {
        width: 100%;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 15px;
            max-width: 400px;
        }

        h1 {
            font-size: 28px;
        }

        h3 {
            font-size: 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# Aplicar los estilos CSS
aplicar_estilos()


# -------------------------
# COMPONENTES
# -------------------------
def titulo(texto, subtitulo=""):
    st.markdown(f"""
    <h1>{texto}</h1>
    <h3>{subtitulo}</h3>
    """, unsafe_allow_html=True)


def mensaje_usuario(texto):
    st.markdown(f"""
    <div style="background-color: #4C8BFF; color: white; padding: 12px; border-radius: 8px; margin: 8px 0; max-width: 75%; margin-left: auto;">
        {texto}
    </div>
    """, unsafe_allow_html=True)


def mensaje_bot(texto):
    st.markdown(f"""
    <div style="background-color: #A5BFCC; color: #4C585B; padding: 12px; border-radius: 8px; margin: 8px 0; max-width: 75%;">
        {texto}
    </div>
    """, unsafe_allow_html=True)


def tarjeta_estadistica(icono, valor, label, color):
    st.markdown(f"""
    <div style="background-color: {color}; color: white; padding: 24px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 32px; margin-bottom: 12px;">{icono}</div>
        <h2>{valor}</h2>
        <p>{label}</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------
# PÁGINAS
# -------------------------

def login():
    titulo("💙 Bienestar Emocional", "Tu espacio seguro para el bienestar")

    email = st.text_input("📧 Email", key="login_email", placeholder="tu@email.com")
    password = st.text_input("🔒 Contraseña", type="password", key="login_password", placeholder="••••••••")
    rol = st.selectbox("👤 Rol", ["Estudiante", "Psicólogo"], key="login_rol")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button("Ingresar", use_container_width=True):
            if not email or not password:
                st.error("⚠️ Completa todos los campos")
            elif not validar_email(email):
                st.error("⚠️ Email inválido")
            else:
                user = buscar_usuario(email, password, rol)
                if user:
                    st.session_state.usuario = user
                    st.session_state.page = "estudiante" if rol == "Estudiante" else "psicologo"
                    st.success("✅ ¡Bienvenido!")
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")

    with col2:
        if st.button("Registrarme", use_container_width=True):
            st.session_state.page = "registro"
            st.rerun()


def registro():
    titulo("✨ Crear cuenta", "Únete a nuestra comunidad")

    col1, col2 = st.columns(2, gap="small")
    with col1:
        nombre = st.text_input("👤 Nombre", key="reg_nombre", placeholder="Juan")
    with col2:
        apellido = st.text_input("👤 Apellido", key="reg_apellido", placeholder="Pérez")

    email = st.text_input("📧 Email", key="reg_email", placeholder="tu@email.com")
    password = st.text_input("🔒 Contraseña", type="password", key="reg_password", placeholder="Mínimo 6 caracteres")
    password_confirm = st.text_input("🔒 Confirmar", type="password", key="reg_password_confirm", placeholder="Repite tu contraseña")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button("Crear cuenta", use_container_width=True):
            errores = []

            if not all([nombre, apellido, email, password, password_confirm]):
                errores.append("Completa todos los campos")
            if nombre and not validar_nombre(nombre):
                errores.append("Nombre inválido")
            if apellido and not validar_nombre(apellido):
                errores.append("Apellido inválido")
            if email and not validar_email(email):
                errores.append("Email inválido")
            if password and not validar_password(password):
                errores.append("Contraseña muy corta")
            if password != password_confirm:
                errores.append("Las contraseñas no coinciden")

            if errores:
                for error in errores:
                    st.error(f"⚠️ {error}")
            else:
                uid = registrar_usuario(nombre.strip(), apellido.strip(), email, password, rol="Estudiante")
                if uid:
                    st.success("✅ ¡Cuenta creada!")
                    st.balloons()
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("❌ Email ya registrado")

    with col2:
        if st.button("Volver", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


def estudiante():
    uid, nombre, apellido, email, rol = st.session_state.usuario

    titulo(f"Hola, {nombre} 👋", "Comparte tus pensamientos")

    st.divider()

    if not st.session_state.chat_history:
        st.markdown(""" 
        <div style='text-align: center; padding: 60px 20px;'>
            <div style='font-size: 64px; margin-bottom: 16px;'>💬</div>
            <h3 style='color: #4C585B; font-size: 20px; font-weight: 700; margin-bottom: 8px;'> 
                Comienza la conversación 
            </h3>
            <p style='color: #7E99A3; font-size: 15px;'> Estoy aquí para escucharte </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                mensaje_usuario(msg['content'])
            else:
                mensaje_bot(msg['content'])

    mensaje = st.chat_input("Escribe cómo te sientes...")

    if mensaje:
        if len(mensaje.strip()) < 3:
            st.warning("⚠️ Mensaje muy corto")
        else:
            st.session_state.chat_history.append({"role": "user", "content": mensaje})

            with st.spinner("Procesando..."):
                resultado = analizar_texto(mensaje)
                data = json.loads(resultado.replace("```json", "").replace("```", ""))

            respuesta = data["mensaje_chat"]
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

            guardar_entrada(mensaje, data["emocion_principal"], data["nivel_estres"], data["recomendacion"], uid)
            st.rerun()

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.page = "login"
        st.session_state.usuario = None
        st.session_state.chat_history = []
        st.rerun()


def psicologo():
    uid, nombre, apellido, email, rol = st.session_state.usuario

    titulo(f"💬 Sesión de Psicologo", "Estado emocional del estudiante")

    st.divider()

    # Verificar sesión
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.session_state.page = "login"
        st.rerun()

    # Obtener las entradas de los estudiantes
    entradas = obtener_entradas()

    if not entradas:
        st.info("No hay entradas aún.")
    else:
        # Mostrar la información de cada entrada con Expander
        for fecha, texto, emocion, estres, recomendacion, nombre_u, apellido_u, email_u in entradas:
            with st.expander(f"Estudiante: {nombre_u} {apellido_u} (Fecha: {fecha})"):
                st.write(f"**Texto de la entrada:** {texto}")
                st.write(f"**Emoción principal:** {emocion}")
                st.write(f"**Nivel de estrés:** {estres}/100")
                st.write(f"**Recomendación:** {recomendacion}")
                st.write("---")

    st.write("---")

    # Botón cerrar sesión
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.page = "login"
        st.session_state.usuario = None
        st.session_state.chat_history = []
        st.rerun()


# -------------------------
# ROUTER
# -------------------------
if st.session_state.page == "login":
    login()
elif st.session_state.page == "registro":
    registro()
elif st.session_state.page == "estudiante":
    estudiante()
elif st.session_state.page == "psicologo":
    psicologo()
