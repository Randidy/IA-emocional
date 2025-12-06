import streamlit as st
import re

from ia.gemini import analizar_texto
from database.database import (
    crear_tablas,
    registrar_usuario,
    guardar_entrada,
    obtener_entradas
)

# Crear tablas al iniciar la app
crear_tablas()

st.title("🧠 Bienestar Emocional Estudiantil")

# --- Login ---
rol = st.selectbox("Soy:", ["Estudiante", "Psicólogo"])
nombre = st.text_input("Nombre")
email = st.text_input("Email")

if st.button("Ingresar"):
    if nombre.strip() != "" and email.strip() != "":
        usuario_id = registrar_usuario(nombre, email, rol)
        st.session_state.usuario = (usuario_id, nombre, email, rol)
        st.success(f"Bienvenido {nombre} ({rol})")
    else:
        st.error("Por favor ingresa tu nombre y email")

# --- Funcionalidad según rol ---
if st.session_state.get("usuario"):
    usuario_id, nombre_u, email_u, rol_u = st.session_state.usuario

    # ---------------------------
    # ESTUDIANTE
    # ---------------------------
    if rol_u == "Estudiante":

        texto = st.text_area("¿Cómo te sientes hoy?")

        if st.button("Analizar y Guardar"):
            if texto.strip() != "":
                resultado = analizar_texto(texto)

                st.write("### Resultado del análisis:")
                st.write(resultado)

                # Extraer emoción / estrés / recomendación
                lineas = resultado.split("\n")
                emocion = ""
                estres = 0
                recomendacion = ""
                recom_flag = False

                for linea in lineas:
                    linea = linea.strip()

                    # Emoción
                    if re.search(r"Emoción", linea, re.IGNORECASE):
                        emocion = linea.split(":", 1)[-1].strip()

                    # Estrés
                    match = re.search(r"(\d{1,3})\s*/\s*100", linea)
                    if match:
                        estres = int(match.group(1))

                    # Recomendación
                    if re.search(r"Recomendación", linea, re.IGNORECASE):
                        recomendacion = linea.split(":", 1)[-1].strip()
                        recom_flag = True
                    elif recom_flag and linea != "":
                        recomendacion += " " + linea
                    elif recom_flag and linea == "":
                        recom_flag = False

                guardar_entrada(texto, emocion, estres, recomendacion, usuario_id)

                st.success("✅ Entrada guardada correctamente en la base de datos")

            else:
                st.error("Escribe algo antes de analizar")

    # ---------------------------
    # PSICÓLOGO
    # ---------------------------
    elif rol_u == "Psicólogo":

        st.write("### Historial de entradas de todos los estudiantes:")
        entradas = obtener_entradas()

        if entradas:
            for fecha, t, emo, est, rec, uid in entradas:
                st.write(
                    f"- **{fecha}** | Usuario ID: {uid} | Emoción: {emo} | "
                    f"Estrés: {est} | Recomendación: {rec}"
                )
        else:
            st.write("No hay entradas guardadas aún.")
