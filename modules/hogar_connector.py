from hogar.service import (
    obtener_resumen_obligaciones,
    obtener_resumen_mes_actual
)


def obtener_dashboard_hogar():

    resumen = obtener_resumen_obligaciones()
    resumen_mes = obtener_resumen_mes_actual()

    return {
        "activas": resumen["total_registros"],
        "total": resumen["total_monto"],
        "compromisos_mes": resumen_mes["cantidad"],
        "total_mes": resumen_mes["total"]
    }