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

# --------------------------------
# 📦 INICIALIZACIÓN
# --------------------------------
crear_tablas()

if "page" not in st.session_state:
    st.session_state.page = "login"


# --------------------------------
# 🎨 ESTILOS
# --------------------------------
st.markdown("""
<style>
body { background-color: white; }
.main {
    padding: 30px;
    border-radius: 20px;
    background: #ffffff;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# 🚪 MODAL CERRAR SESIÓN
# --------------------------------
@st.dialog("Confirmación")
def modal_cerrar_sesion():
    st.write("¿Estás seguro que deseas cerrar sesión?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sí, salir", type="primary", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.usuario = None
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()


# --------------------------------
# 🔐 LOGIN
# --------------------------------
def pantalla_login():
    st.title("🧠 Bienestar Emocional Estudiantil")
    st.subheader("🔑 Iniciar sesión")

    rol = st.selectbox("Soy:", ["Estudiante", "Psicólogo"])
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    email = st.text_input("Email")

    if st.button("Ingresar", use_container_width=True):

        if len(nombre.strip()) < 3 or len(apellido.strip()) < 3:
            st.warning("⚠️ Nombre y apellido deben tener al menos 3 caracteres.")
            return

        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email):
            st.warning("⚠️ Ingresa un correo válido.")
            return

        usuario_id = registrar_usuario(nombre, apellido, email, rol)

        st.session_state.usuario = (
            usuario_id,
            nombre,
            apellido,
            email,
            rol
        )

        st.session_state.page = "estudiante" if rol == "Estudiante" else "psicologo"
        st.rerun()


# --------------------------------
# 🟩 ESTUDIANTE
# --------------------------------
def pantalla_estudiante():
    st.title("🧑‍🎓 Registro emocional del estudiante")

    if "usuario" not in st.session_state or st.session_state.usuario is None:
        st.session_state.page = "login"
        st.rerun()

    usuario_id, nombre_u, apellido_u, email_u, rol_u = st.session_state.usuario

    st.write(f"👋 Hola **{nombre_u} {apellido_u}**, cuéntame cómo te sientes hoy")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        texto = st.text_area("¿Cómo te sientes hoy?")
        enviar = st.form_submit_button("Enviar")

    if enviar and texto.strip():
        st.session_state.chat_history.append(
            {"role": "user", "message": texto}
        )

        resultado = analizar_texto(texto)

        try:
            data = json.loads(
                resultado.replace("```json", "").replace("```", "").strip()
            )
        except:
            st.error("⚠️ Error interpretando la respuesta de la IA")
            return

        st.session_state.chat_history.append(
            {"role": "bot", "message": data.get("mensaje_chat", "")}
        )

        guardar_entrada(
            texto,
            data.get("emocion_principal", ""),
            data.get("nivel_estres", 0),
            data.get("recomendacion", ""),
            usuario_id
        )

    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**{nombre_u}:** {chat['message']}")
        else:
            st.markdown(f"**Sistema:** {chat['message']}")

    st.divider()

    if st.button("Cerrar sesión", use_container_width=True):
        modal_cerrar_sesion()


# --------------------------------
# 🟪 PSICÓLOGO
# --------------------------------
def pantalla_psicologo():
    st.title("🧑‍⚕️ Panel del Psicólogo")
    st.write("### 🗂️ Historial emocional de los estudiantes")

    entradas = obtener_entradas()

    if not entradas:
        st.info("No hay entradas aún.")
        return

    historial_por_fecha = {}

    for fecha, texto, emo, est, rec, nombre, apellido, email in entradas:
        fecha_simple = fecha.split(" ")[0]
        historial_por_fecha.setdefault(fecha_simple, []).append(
            (texto, emo, est, rec, nombre, apellido, email)
        )

    for fecha, items in historial_por_fecha.items():
        with st.expander(f"📅 Fecha: {fecha}"):
            for texto, emo, est, rec, nombre, apellido, email in items:
                st.write(f"👤 **Estudiante:** {nombre} {apellido}")
                st.write(f"📧 **Email:** {email}")
                st.write(f"📝 **Texto:** {texto}")
                st.write(f"💭 **Emoción:** {emo}")
                st.write(f"📊 **Estrés:** {est}/100")
                st.write(f"💡 **Recomendación:** {rec}")
                st.divider()

    if st.button("Cerrar sesión", use_container_width=True):
        modal_cerrar_sesion()


# --------------------------------
# 🚦 CONTROLADOR
# --------------------------------
if st.session_state.page == "login":
    pantalla_login()
elif st.session_state.page == "estudiante":
    pantalla_estudiante()
elif st.session_state.page == "psicologo":
    pantalla_psicologo()
