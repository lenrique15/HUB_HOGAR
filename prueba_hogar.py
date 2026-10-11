from hogar.service import (
    agregar_obligacion,
    obtener_obligaciones
)

agregar_obligacion(
    "Internet",
    "Servicio",
    649,
    "Mensual",
    "2026-10-15"
)

print(
    obtener_obligaciones()
)