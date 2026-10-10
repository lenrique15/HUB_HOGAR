import os
import sqlite3

DB_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/04_PROYECTOS_PYTHON/AFI/DATA/finances.db"
)


def obtener_resumen_financiero():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total movimientos
    cursor.execute("SELECT COUNT(*) FROM movimientos")
    movimientos = cursor.fetchone()[0]

    # Total ingresos
    cursor.execute("""
        SELECT COALESCE(SUM(monto), 0)
        FROM movimientos
        WHERE tipo = 'Ingreso'
    """)
    ingresos = cursor.fetchone()[0]

    # Total gastos
    cursor.execute("""
        SELECT COALESCE(SUM(monto), 0)
        FROM movimientos
        WHERE tipo = 'Gasto'
    """)
    gastos = cursor.fetchone()[0]

    conn.close()

    return {
        "movimientos": movimientos,
        "ingresos": ingresos,
        "gastos": gastos,
        "balance": ingresos - gastos
    }