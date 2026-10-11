import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

def actualizar_obligacion(
    obligacion_id,
    nombre,
    categoria,
    monto,
    frecuencia,
    proxima_fecha
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE obligaciones
        SET
            nombre = ?,
            categoria = ?,
            monto = ?,
            frecuencia = ?,
            proxima_fecha = ?
        WHERE id = ?
    """, (
        nombre,
        categoria,
        monto,
        frecuencia,
        proxima_fecha,
        obligacion_id
    ))

    conn.commit()
    conn.close()

def desactivar_obligacion(obligacion_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE obligaciones
        SET activo = 0
        WHERE id = ?
        """,
        (obligacion_id,)
    )

    conn.commit()
    conn.close()

def obtener_resumen_obligaciones():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*),
               COALESCE(SUM(monto), 0)
        FROM obligaciones
        WHERE activo = 1
    """)

    total_registros, total_monto = cursor.fetchone()

    conn.close()

    return {
        "total_registros": total_registros,
        "total_monto": total_monto
    }

def obtener_resumen_mes_actual():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT monto, proxima_fecha
        FROM obligaciones
        WHERE activo = 1
    """)

    registros = cursor.fetchall()

    conn.close()

    hoy = datetime.now()

    total = 0
    cantidad = 0

    for monto, fecha in registros:

        try:

            fecha_pago = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            )

            if (
                fecha_pago.month == hoy.month
                and fecha_pago.year == hoy.year
            ):

                total += monto
                cantidad += 1

        except:

            pass

    return {
        "cantidad": cantidad,
        "total": round(total, 2)
    }

def marcar_pagado(obligacion_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT frecuencia, proxima_fecha
        FROM obligaciones
        WHERE id = ?
    """, (obligacion_id,))

    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return

    frecuencia, fecha = resultado

    fecha_actual = datetime.strptime(
        fecha,
        "%Y-%m-%d"
    )

    if frecuencia == "Semanal":
        nueva_fecha = fecha_actual + relativedelta(weeks=1)

    elif frecuencia == "Quincenal":
        nueva_fecha = fecha_actual + relativedelta(days=15)

    elif frecuencia == "Mensual":
        nueva_fecha = fecha_actual + relativedelta(months=1)

    elif frecuencia == "Bimestral":
        nueva_fecha = fecha_actual + relativedelta(months=2)

    elif frecuencia == "Trimestral":
        nueva_fecha = fecha_actual + relativedelta(months=3)

    elif frecuencia == "Semestral":
        nueva_fecha = fecha_actual + relativedelta(months=6)

    elif frecuencia == "Anual":
        nueva_fecha = fecha_actual + relativedelta(years=1)

    else:
        conn.close()
        return

    cursor.execute("""
        UPDATE obligaciones
        SET proxima_fecha = ?
        WHERE id = ?
    """, (
        nueva_fecha.strftime("%Y-%m-%d"),
        obligacion_id
    ))

    conn.commit()
    conn.close()