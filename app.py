import streamlit as st
import re
import json

from ia.gemini import analizar_texto
from database.database import (
    crear_tablas,
    registrar_usuario,
    guardar_entrada,
    obtener_entradas
)

# Crear tablas
crear_tablas()

# Inicializar estado de página
if "page" not in st.session_state:
    st.session_state.page = "login"

if "confirm_logout" not in st.session_state:
    st.session_state.confirm_logout = False


# --------------------------------
# 🎨 ESTILOS PERSONALIZADOS + MODAL
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

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.55);
        backdrop-filter: blur(3px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .modal-box {
        background: white;
        padding: 25px;
        border-radius: 12px;
        width: 360px;
        box-shadow: 0px 4px 30px rgba(0,0,0,0.30);
        text-align: center;
        color: #1a1a1a;
    }

    .modal-box h4 {
        font-size: 20px;
        margin-bottom: 8px;
        font-weight: 700;
        color: #000000;
    }

    .modal-box p {
        font-size: 15px;
        color: #444444;
    }
    </style>
""", unsafe_allow_html=True)


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
# 📗 FUNCION MODAL PERSONALIZADO
# --------------------------------
def modal_confirmacion():
    st.markdown("""
        <div class="modal-overlay">
            <div class="modal-box">
                <h4>¿Deseas cerrar sesión?</h4>
                <p>Tu sesión actual se cerrará.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sí, cerrar", key="cerrar_sesion_si"):
            st.session_state.page = "login"
            st.session_state.confirm_logout = False
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("Cancelar", key="cerrar_sesion_no"):
            st.session_state.confirm_logout = False
            st.rerun()


# --------------------------------
# 🟩 PANTALLA ESTUDIANTE
# --------------------------------
def pantalla_estudiante():
    st.title("🧑‍🎓 Registro emocional del estudiante")
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
            st.write(resultado)
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

    # Botón cerrar
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.confirm_logout = True

    if st.session_state.confirm_logout:
        modal_confirmacion()


# --------------------------------
# 🟪 PANTALLA PSICÓLOGO
# --------------------------------
def pantalla_psicologo():
    st.title("🧑‍⚕️ Panel del Psicólogo")
    st.write("### 🗂️ Historial agrupado por fecha:")

    entradas = obtener_entradas()

    if not entradas:
        st.info("No hay entradas aún.")
        return

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

    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.confirm_logout = True

    if st.session_state.confirm_logout:
        modal_confirmacion()


# --------------------------------
# CONTROLADOR PRINCIPAL
# --------------------------------
if st.session_state.page == "login":
    pantalla_login()
elif st.session_state.page == "estudiante":
    pantalla_estudiante()
elif st.session_state.page == "psicologo":
    pantalla_psicologo()
