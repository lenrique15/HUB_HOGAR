# HUB HOGAR
## Estado del Proyecto
### Fecha: 10/10/2026

---

# Visión General

HUB Hogar es el centro de control familiar que integra:

- AFI (Asistente Financiero Inteligente)
- ADP (Administrador de Respaldos)
- Módulo propio de Obligaciones del Hogar

La filosofía es:

AFI = Estado financiero actual

ADP = Estado de respaldos

Hogar = Compromisos y obligaciones futuras

Dashboard = Vista ejecutiva unificada

---

# Estado Actual

## Dashboard

Actualmente muestra:

### Disponible después de compromisos

Calculado como:

Balance AFI
-
Compromisos del mes actual

Este indicador es considerado el principal indicador del sistema.

### Obligaciones

Muestra:

- Obligaciones activas
- Compromisos del mes
- Total del mes
- Total registrado

### Finanzas

Datos provenientes de AFI:

- Balance
- Ingresos
- Gastos
- Movimientos
- Último movimiento

### Respaldos

Datos provenientes de ADP:

- Total de respaldos
- Último respaldo

---

# Arquitectura

## Estructura

```text
HUB_HOGAR/

├── app.py

├── modules/
│   ├── afi_connector.py
│   ├── adp_connector.py
│   └── hogar_connector.py

├── hogar/
│   ├── database.py
│   ├── service.py
│   └── view.py

├── data/
│   └── hogar.db

├── assets/

└── config/
```

---

# Módulo Hogar

## Base de datos

Archivo:

```text
data/hogar.db
```

## Tabla

```sql
obligaciones
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    monto REAL,
    frecuencia TEXT,
    proxima_fecha TEXT,
    activo INTEGER DEFAULT 1
)
```

---

# Funcionalidades Implementadas

## CRUD completo

### Crear

✅ Nueva Obligación

### Leer

✅ Tabla de obligaciones ordenada cronológicamente.

### Editar

✅ Modificación completa de obligaciones.

### Desactivar

✅ Desactivación lógica mediante activo = 0.

---

# Marcar Pagado

✅ Implementado.

Avanza automáticamente la fecha según la frecuencia configurada.

Frecuencias:

- Semanal
- Quincenal
- Mensual
- Bimestral
- Trimestral
- Semestral
- Anual

Utiliza:

```python
python-dateutil
relativedelta
```

---

# Navegación

✅ Dashboard ↔ Hogar

Métodos:

```python
mostrar_dashboard()
mostrar_hogar()
```

---

# Indicadores Implementados

## Total registrado

Suma de obligaciones activas.

## Compromisos del mes

Cantidad y monto de obligaciones correspondientes al mes actual.

## Disponible después de compromisos

Fórmula:

```text
Balance AFI - Compromisos del mes
```

Indicador principal del Dashboard.

---

# Mejoras Pendientes

## Alta prioridad

### Fechas amigables

Mostrar:

```text
18/10/2026
```

en lugar de:

```text
2026-10-18
```

Aplicar en:

- Tabla
- Alta de obligaciones
- Edición de obligaciones
- Dashboard

Manteniendo en SQLite:

```text
YYYY-MM-DD
```

### Confirmación antes de marcar pagado

```text
¿Marcar obligación como pagada?
```

## Prioridad media

### Próxima obligación en Dashboard

Mostrar:

- Próximo vencimiento
- Fecha
- Monto

### Indicador de riesgo

Comparar balance AFI vs compromisos.

---

# Estado General

Versión conceptual:

HUB 0.3

Estado:

✅ Estable
✅ Integrado con AFI
✅ Integrado con ADP
✅ CRUD completo de Obligaciones
✅ Indicadores ejecutivos
✅ Persistencia SQLite
✅ Navegación funcional

Listo para continuar el desarrollo desde este punto.
