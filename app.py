import streamlit as st
import sqlite3
from datetime import datetime
import os
import re

# Importa tu función de análisis (o simula si no tienes API)
from ia.gemini import analizar_texto

# --- Configuración de SQLite AHAHAHAHAHAHHA ---
DB_PATH = "data/emotional.db"

if not os.path.exists("data"):
    os.makedirs("data")

# --- Funciones de DB ---
def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT UNIQUE,
            rol TEXT
        )
    """)
    # Tabla de entradas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            texto TEXT,
            emocion TEXT,
            estres INTEGER,
            recomendacion TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(nombre, email, rol):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    if not usuario:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, rol) VALUES (?, ?, ?)",
            (nombre, email, rol)
        )
        conn.commit()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
    conn.close()
    return usuario

def guardar_entrada(texto, emocion, estres, recomendacion, user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entradas (fecha, texto, emocion, estres, recomendacion, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), texto, emocion, estres, recomendacion, user_id))
    conn.commit()
    conn.close()

def obtener_entradas(usuario_id=None):
    conn = conectar()
    cursor = conn.cursor()
    if usuario_id:
        cursor.execute("""
            SELECT fecha, texto, emocion, estres, recomendacion
            FROM entradas WHERE user_id = ? ORDER BY id DESC
        """, (usuario_id,))
    else:
        cursor.execute("""
            SELECT fecha, texto, emocion, estres, recomendacion
            FROM entradas ORDER BY id DESC
        """)
    filas = cursor.fetchall()
    conn.close()
    return filas

# Crear tablas al inicio
crear_tablas()

# --- Streamlit UI ---
st.title("🧠 Bienestar Emocional Estudiantil")

# --- Login / Registro ---
rol = st.selectbox("Soy:", ["Estudiante", "Psicólogo"])
nombre = st.text_input("Nombre")
email = st.text_input("Email")

if st.button("Ingresar"):
    if nombre.strip() != "" and email.strip() != "":
        usuario = registrar_usuario(nombre, email, rol)
        st.session_state.usuario = usuario
        st.success(f"Bienvenido {usuario[1]} ({usuario[3]})")
    else:
        st.error("Por favor ingresa tu nombre y email")

# --- Funcionalidad según rol ---
if st.session_state.get("usuario"):
    usuario = st.session_state.usuario

    # Si es estudiante, puede registrar emociones
    if usuario[3] == "Estudiante":
        texto = st.text_area("¿Cómo te sientes hoy?")
        if st.button("Analizar y Guardar"):
            if texto.strip() != "":
                resultado = analizar_texto(texto)
                st.write("### Resultado del análisis:")
                st.write(resultado)

                # Extraer emoción, estrés y recomendación
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

                guardar_entrada(texto, emocion, estres, recomendacion, usuario[0])
                st.success("✅ Entrada guardada correctamente en la base de datos")
            else:
                st.error("Escribe algo antes de analizar")

    # Si es psicólogo, puede ver todas las entradas
    elif usuario[3] == "Psicólogo":
        st.write("### Historial de entradas de todos los estudiantes:")
        entradas = obtener_entradas()
        if entradas:
            for fecha, t, emo, est, rec in entradas:
                st.write(f"- **{fecha}** | Emoción: {emo}, Estrés: {est}, Recomendación: {rec}")
        else:
            st.write("No hay entradas guardadas aún.")
