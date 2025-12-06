import sqlite3
from datetime import datetime
import os
# database/database.py
# --- Configuración ---
DB_PATH = "data/emotional.db"

if not os.path.exists("data"):
    os.makedirs("data")


# --- Conexión ---
def conectar():
    return sqlite3.connect(DB_PATH)


# --- Creación de tablas ---
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabla usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT UNIQUE,
            rol TEXT
        )
    """)

    # Tabla entradas SIN user_id (por si existe vieja)
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

    # Agregar user_id si no existe
    try:
        cursor.execute("ALTER TABLE entradas ADD COLUMN user_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Ya existe

    conn.commit()
    conn.close()


# --- Registrar usuario ---
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


# --- Guardar entrada ---
def guardar_entrada(texto, emocion, estres, recomendacion, user_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entradas (fecha, texto, emocion, estres, recomendacion, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          texto, emocion, estres, recomendacion, user_id))

    conn.commit()
    conn.close()


# --- Obtener entradas ---
def obtener_entradas(user_id=None):
    conn = conectar()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT fecha, texto, emocion, estres, recomendacion
            FROM entradas
            WHERE user_id=?
            ORDER BY id DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT fecha, texto, emocion, estres, recomendacion, user_id
            FROM entradas
            ORDER BY id DESC
        """)

    datos = cursor.fetchall()
    conn.close()
    return datos
