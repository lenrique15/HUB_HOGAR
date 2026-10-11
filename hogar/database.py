import sqlite3


DB_PATH = "data/hogar.db"


def crear_base_datos():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS obligaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            monto REAL,
            frecuencia TEXT,
            proxima_fecha TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()