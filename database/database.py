import streamlit as st
import sqlite3
from datetime import datetime
import os
import re
from ia.gemini import analizar_texto  # tu función de análisis de emociones

# --- Configuración de SQLite ---
DB_PATH = "data/emotional.db"

if not os.path.exists("data"):
    os.makedirs("data")

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
            recomendacion TEXT
        )
    """)

    # Agregar columna user_id si no existe
    try:
        cursor.execute("ALTER TABLE entradas ADD COLUMN user_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Ya existe

    conn.commit()
    conn.close()

def registrar_usuario(nombre, email, rol):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (nombre, email, rol)
        VALUES (?, ?, ?)
    """, (nombre, email, rol))
    conn.commit()
    cursor.execute("SELECT id FROM usuarios WHERE email=?", (email,))
    usuario_id = cursor.fetchone()[0]
    conn.close()
    return usuario_id

def guardar_entrada(texto, emocion, estres, recomendacion, user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entradas (fecha, texto, emocion, estres, recomendacion, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), texto, emocion, estres, recomendacion, user_id))
    conn.commit()
    conn.close()

def obtener_entradas(user_id=None):
    conn = conectar()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT fecha, texto, emocion, estres, recomendacion FROM entradas WHERE user_id=? ORDER BY id DESC", (user_id,))
    else:
        cursor.execute("SELECT fecha, texto, emocion, estres, recomendacion, user_id FROM entradas ORDER BY id DESC")
    filas = cursor.fetchall()
    conn.close()
    return filas

# Crear tablas al inicio
crear_tablas()

# --- Streamlit UI ---
st.title("🧠 Bienestar Emocional Estudiantil")

# --- Login / Registro ---
st.subheader("🔑 Identificación")
nombre = st.text_input("Nombre")
email = st.text_input("Email")
rol = st.selectbox("Rol", ["Estudiante", "Psicólogo"])

if st.button("Ingresar"):
    if nombre.strip() == "" or email.strip() == "":
        st.warning("Debes ingresar nombre y email")
    else:
        user_id = registrar_usuario(nombre.strip(), email.strip(), rol)
        st.success(f"Bienvenido {nombre}! Rol: {rol}")

        if rol == "Estudiante":
            st.subheader("📝 Expresa cómo te sientes")
            texto = st.text_area("Describe tu estado emocional")

            if st.button("Analizar y guardar"):
                if texto.strip() == "":
                    st.warning("Escribe algo antes de analizar")
                else:
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
                        if re.search(r"Emoción", linea, re.IGNORECASE):
                            emocion = linea.split(":", 1)[-1].strip()
                        match = re.search(r"(\d{1,3})\s*/\s*100", linea)
                        if match:
                            estres = int(match.group(1))
                        if re.search(r"Recomendación", linea, re.IGNORECASE):
                            recomendacion = linea.split(":", 1)[-1].strip()
                            recom_flag = True
                        elif recom_flag and linea != "":
                            recomendacion += " " + linea
                        elif recom_flag and linea == "":
                            recom_flag = False

                    guardar_entrada(texto, emocion, estres, recomendacion, user_id)
                    st.success("✅ Entrada guardada correctamente")

        elif rol == "Psicólogo":
            st.subheader("📋 Entradas de estudiantes")
            entradas = obtener_entradas()
            if entradas:
                for fecha, texto, emo, est, rec, uid in entradas:
                    st.write(f"- **{fecha}** | Usuario ID: {uid} | Emoción: {emo} | Estrés: {est} | Recomendación: {rec}")
            else:
                st.write("No hay entradas registradas todavía")
