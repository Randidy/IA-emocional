import sqlite3
from datetime import datetime
import os
import hashlib

DB_PATH = "data/emotional.db"

if not os.path.exists("data"):
    os.makedirs("data")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            email TEXT UNIQUE,
            password TEXT,
            rol TEXT
        )
    """)

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

    # 🔹 Insertar psicólogo inicial si no existe
    cursor.execute("""
        SELECT * FROM usuarios WHERE rol = 'Psicólogo'
    """)
    if not cursor.fetchone():
        # Definir psicólogo
        nombre = "Admin"
        apellido = "Psicologo"
        email = "psicologo@dominio.com"
        password = hash_password("psico123")  # Contraseña inicial
        rol = "Psicólogo"
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, email, password, rol)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, apellido, email, password, rol))

    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario(nombre, apellido, email, password, rol="Estudiante"):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, email, password, rol)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, apellido, email, hash_password(password), rol))

        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def buscar_usuario(email, password, rol):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, apellido, email, rol
        FROM usuarios
        WHERE email = ? AND password = ? AND rol = ?
    """, (email, hash_password(password), rol))

    user = cursor.fetchone()
    conn.close()
    return user

def guardar_entrada(texto, emocion, estres, recomendacion, user_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entradas
        (fecha, texto, emocion, estres, recomendacion, user_id)
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

    data = cursor.fetchall()
    conn.close()
    return data
