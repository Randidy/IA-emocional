import sqlite3
from datetime import datetime
import os

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

    # Tabla usuarios (CON APELLIDO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            email TEXT UNIQUE,
            rol TEXT
        )
    """)

    # Tabla entradas
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


# --- Registrar usuario ---
def registrar_usuario(nombre, apellido, email, rol):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (nombre, apellido, email, rol)
        VALUES (?, ?, ?, ?)
    """, (nombre, apellido, email, rol))

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
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        texto,
        emocion,
        estres,
        recomendacion,
        user_id
    ))

    conn.commit()
    conn.close()


# --- Obtener entradas (CON NOMBRE Y APELLIDO) ---
def obtener_entradas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.fecha,
            e.texto,
            e.emocion,
            e.estres,
            e.recomendacion,
            u.nombre,
            u.apellido,
            u.email
        FROM entradas e
        JOIN usuarios u ON e.user_id = u.id
        ORDER BY e.id DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos
