import sqlite3

DB_PATH = "data/hogar.db"


def agregar_obligacion(
    nombre,
    categoria,
    monto,
    frecuencia,
    proxima_fecha
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO obligaciones (
            nombre,
            categoria,
            monto,
            frecuencia,
            proxima_fecha
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nombre,
        categoria,
        monto,
        frecuencia,
        proxima_fecha
    ))

    conn.commit()
    conn.close()


def obtener_obligaciones():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            categoria,
            monto,
            frecuencia,
            proxima_fecha
        FROM obligaciones
        WHERE activo = 1
        ORDER BY proxima_fecha
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos