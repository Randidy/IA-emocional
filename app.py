import streamlit as st
import re
import json

# Asegúrate de tener estas librerías instaladas y tus archivos en la ruta correcta
from ia.gemini import analizar_texto
from database.database import (
    crear_tablas,
    registrar_usuario,
    guardar_entrada,
    obtener_entradas
)

# Crear tablas al inicio
crear_tablas()

# Inicializar estado de página
if "page" not in st.session_state:
    st.session_state.page = "login"

# --------------------------------
# 🎨 ESTILOS PERSONALIZADOS
# --------------------------------
st.markdown("""
    <style>
    body {
        background-color: white;
    }
    .main {
        padding: 30px;
        border-radius: 20px;
        background: #ffffff;
    }
    /* El CSS del modal antiguo se eliminó para usar el nativo de Streamlit */
    </style>
""", unsafe_allow_html=True)


# --------------------------------
# 🚪 FUNCION MODAL (NATIVA)
# --------------------------------
@st.dialog("Confirmación")
def modal_cerrar_sesion():
    st.write("¿Estás seguro que deseas cerrar sesión?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sí, salir", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.usuario = None
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


# --------------------------------
# 🔐 PANTALLA LOGIN
# --------------------------------
def pantalla_login():
    st.title("🧠 Bienestar Emocional Estudiantil")
    st.subheader("🔑 Iniciar sesión")

    rol = st.selectbox("Soy:", ["Estudiante", "Psicólogo"])
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")

    if st.button("Ingresar", use_container_width=True):

        # VALIDACIÓN: nombre
        if len(nombre.strip()) < 3:
            st.warning("⚠️ El nombre debe tener al menos 3 caracteres.")
            return

        # VALIDACIÓN: email correcto
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            st.warning("⚠️ Ingresa un correo válido (ejemplo: usuario@correo.com).")
            return

        usuario_id = registrar_usuario(nombre, email, rol)
        st.session_state.usuario = (usuario_id, nombre, email, rol)

        st.session_state.page = "estudiante" if rol == "Estudiante" else "psicologo"
        st.rerun()


# --------------------------------
# 🟩 PANTALLA ESTUDIANTE
# --------------------------------
def pantalla_estudiante():
    st.title("🧑‍🎓 Registro emocional del estudiante")

    # Verificar sesión
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.session_state.page = "login"
        st.rerun()

    usuario_id, nombre_u, email_u, rol_u = st.session_state.usuario

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        texto = st.text_area("¿Cómo te sientes hoy?")
        enviar = st.form_submit_button("Enviar")

    if enviar and texto.strip():
        st.session_state.chat_history.append({"role": "user", "message": texto})

        resultado = analizar_texto(texto)

        try:
            data = json.loads(resultado.replace("```json", "").replace("```", "").strip())
        except:
            st.error("⚠️ Error interpretando la respuesta de la IA")
            return

        mensaje_chat = data.get("mensaje_chat", "")
        emocion = data.get("emocion_principal", "")
        estres = data.get("nivel_estres", 0)
        recomendacion = data.get("recomendacion", "")

        st.session_state.chat_history.append({"role": "bot", "message": mensaje_chat})

        guardar_entrada(texto, emocion, estres, recomendacion, usuario_id)

    # Mostrar chat
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**Tú:** {chat['message']}")
        else:
            st.markdown(f"**Sistema:** {chat['message']}")

    st.write("---")

    # Botón cerrar sesión con Modal
    if st.button("Cerrar sesión", use_container_width=True):
        modal_cerrar_sesion()


# --------------------------------
# 🟪 PANTALLA PSICÓLOGO
# --------------------------------
def pantalla_psicologo():
    st.title("🧑‍⚕️ Panel del Psicólogo")

    # Verificar sesión
    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.session_state.page = "login"
        st.rerun()

    st.write("### 🗂️ Historial agrupado por fecha:")

    entradas = obtener_entradas()

    if not entradas:
        st.info("No hay entradas aún.")
    else:
        historial_por_fecha = {}

        for fecha, texto, emo, est, rec, uid in entradas:
            fecha_simple = fecha.split(" ")[0]
            historial_por_fecha.setdefault(fecha_simple, []).append(
                (texto, emo, est, rec, uid)
            )

        for fecha, items in historial_por_fecha.items():
            with st.expander(f"📅 Fecha: {fecha}"):
                for texto, emo, est, rec, uid in items:
                    st.write(f"**Usuario ID:** {uid}")
                    st.write(f"**Texto:** {texto}")
                    st.write(f"**Emoción:** {emo}")
                    st.write(f"**Estrés:** {est}/100")
                    st.write(f"**Recomendación:** {rec}")
                    st.write("---")

    st.write("---")

    # Botón cerrar sesión con Modal
    if st.button("Cerrar sesión", use_container_width=True):
        modal_cerrar_sesion()


# --------------------------------
# CONTROLADOR PRINCIPAL
# --------------------------------
if st.session_state.page == "login":
    pantalla_login()
elif st.session_state.page == "estudiante":
    pantalla_estudiante()
elif st.session_state.page == "psicologo":
    pantalla_psicologo()