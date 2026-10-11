import os
from pathlib import Path


def obtener_resumen_respaldos():

    carpeta = Path(
        os.path.expanduser(
            "~/Library/Mobile Documents/com~apple~CloudDocs/ADP Backups"
        )
    )

    if not carpeta.exists():

        return {
            "total_respaldos": 0,
            "ultimo_respaldo": "-"
        }

    sesiones = [
        s for s in carpeta.iterdir()
        if s.is_dir()
    ]

    total_respaldos = len(sesiones)

    if not sesiones:

        return {
            "total_respaldos": 0,
            "ultimo_respaldo": "-"
        }

    ultimo = max(
        sesiones,
        key=lambda s: s.stat().st_mtime
    )

    fecha = ultimo.name

    fecha_legible = (
        f"{fecha[6:8]}/"
        f"{fecha[4:6]}/"
        f"{fecha[0:4]}"
    )

    carpetas = [
        item.name
        for item in ultimo.iterdir()
        if item.is_dir()
    ]

    return {
        "total_respaldos": total_respaldos,
        "ultimo_respaldo": fecha_legible,
        "carpetas": carpetas
    }