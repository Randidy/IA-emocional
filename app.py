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
    .block-container {
        padding-top: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)


# --------------------------------
# 🟦 PANTALLA: LOGIN
# --------------------------------
def pantalla_login():
    st.title("🧠 Bienestar Emocional Estudiantil")
    st.subheader("🔑 Iniciar sesión")

    rol = st.selectbox("Soy:", ["Estudiante", "Psicólogo"])
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")

    if st.button("Ingresar", use_container_width=True):

        # VALIDACIÓN MEJORADA
        if len(nombre.strip()) < 3:
            st.warning("⚠️ El nombre debe tener al menos 3 caracteres.")
            return

        # REGEX CORREGIDO
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            st.warning("⚠️ Ingresa un correo válido (ejemplo: usuario@correo.com).")
            return

        # Registrar usuario
        usuario_id = registrar_usuario(nombre, email, rol)
        st.session_state.usuario = (usuario_id, nombre, email, rol)

        st.session_state.page = "estudiante" if rol == "Estudiante" else "psicologo"
        st.rerun()


# --------------------------------
# 🟩 PANTALLA: ESTUDIANTE
# --------------------------------
def pantalla_estudiante():
    st.title("🧑‍🎓 Registro emocional del estudiante")
    usuario_id, nombre_u, email_u, rol_u = st.session_state.usuario

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        texto = st.text_area("¿Cómo te sientes hoy?")
        enviar = st.form_submit_button("Enviar")

    if enviar and texto.strip() != "":
        st.session_state.chat_history.append({"role": "user", "message": texto})

        resultado = analizar_texto(texto)

        try:
            resultado_limpio = resultado.replace("```json", "").replace("```", "").strip()
            data = json.loads(resultado_limpio)

            mensaje_chat = data.get("mensaje_chat", "")
            emocion = data.get("emocion_principal", "")
            estres = data.get("nivel_estres", 0)
            recomendacion = data.get("recomendacion", "")

        except Exception:
            st.error("⚠️ Error interpretando la respuesta de la IA")
            st.write(resultado)
            return

        st.session_state.chat_history.append({"role": "bot", "message": mensaje_chat})

        guardar_entrada(texto, emocion, estres, recomendacion, usuario_id)

    # Mostrar conversación
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**Tú:** {chat['message']}")
        else:
            st.markdown(f"**Sistema:** {chat['message']}")

    # ------------------------------
    # CONFIRMACIÓN CIERRE SESIÓN
    # ------------------------------
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.confirm_logout = True

    if st.session_state.confirm_logout:
        with st.modal("¿Deseas cerrar sesión?"):
            st.write("Tu sesión actual se cerrará.")
            c1, c2 = st.columns(2)

            with c1:
                if st.button("Sí, cerrar"):
                    st.session_state.page = "login"
                    st.session_state.chat_history = []
                    st.session_state.confirm_logout = False
                    st.rerun()

            with c2:
                if st.button("Cancelar"):
                    st.session_state.confirm_logout = False
                    st.rerun()


# --------------------------------
# 🟪 PANTALLA: PSICÓLOGO
# --------------------------------
def pantalla_psicologo():
    st.title("🧑‍⚕️ Panel del Psicólogo")
    st.write("### 🗂️ Historial agrupado por fecha:")

    entradas = obtener_entradas()

    if not entradas:
        st.info("No hay entradas aún.")
        return

    # ------------------------------------------------------------
    #  AGREGACIÓN POR FECHA
    # ------------------------------------------------------------
    historial_por_fecha = {}

    for fecha, texto, emo, est, rec, uid in entradas:
        fecha_simple = fecha.split(" ")[0]  # yyyy-mm-dd

        if fecha_simple not in historial_por_fecha:
            historial_por_fecha[fecha_simple] = []

        historial_por_fecha[fecha_simple].append(
            (texto, emo, est, rec, uid)
        )

    # Mostrar agrupado
    for fecha, items in historial_por_fecha.items():
        with st.expander(f"📅 Fecha: {fecha}"):
            for texto, emo, est, rec, uid in items:
                st.write(f"**Usuario ID:** {uid}")
                st.write(f"**Texto:** {texto}")
                st.write(f"**Emoción:** {emo}")
                st.write(f"**Estrés:** {est}/100")
                st.write(f"**Recomendación:** {rec}")
                st.write("---")

    # ------------------------------
    # CONFIRMACIÓN CIERRE SESIÓN
    # ------------------------------
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.confirm_logout = True

    if st.session_state.confirm_logout:
        with st.modal("¿Deseas cerrar sesión?"):
            st.write("Tu sesión actual se cerrará.")
            c1, c2 = st.columns(2)

            with c1:
                if st.button("Sí, cerrar"):
                    st.session_state.page = "login"
                    st.session_state.confirm_logout = False
                    st.rerun()

            with c2:
                if st.button("Cancelar"):
                    st.session_state.confirm_logout = False
                    st.rerun()


# --------------------------------
# CONTROLADOR DE PANTALLAS
# --------------------------------
if st.session_state.page == "login":
    pantalla_login()

elif st.session_state.page == "estudiante":
    pantalla_estudiante()

elif st.session_state.page == "psicologo":
    pantalla_psicologo()
