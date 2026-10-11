import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess

from modules.afi_connector import obtener_resumen_financiero
from modules.afi_connector import obtener_movimientos_mes_actual
from modules.adp_connector import obtener_resumen_respaldos
from modules.hogar_connector import obtener_dashboard_hogar
from hogar.service import obtener_obligaciones_mes_actual
from hogar.view import HogarView



class HubHogar:

    def __init__(self, root):
        self.root = root

        resumen = obtener_resumen_financiero()
        respaldos = obtener_resumen_respaldos()

        root.title("HUB Hogar 0.1 ALPHA")

        width = 1400
        height = 900

        root.update_idletasks()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        root.geometry(f"{width}x{height}+{x}+{y}")

        # Frame lateral
        sidebar = ttk.Frame(root, padding=10)
        sidebar.pack(side=LEFT, fill=Y)

        ttk.Label(
            sidebar,
            text="🏠 HUB HOGAR",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)

        ttk.Button(
            sidebar,
            text="🏠 Dashboard",
            command=self.mostrar_dashboard
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="💰 Finanzas",
            command=self.mostrar_finanzas
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="☁️ Respaldos",
            command=self.mostrar_respaldos
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="Hogar",
            command=self.mostrar_hogar
        ).pack(fill=X, pady=5)

        # Área principal
        self.main = ttk.Frame(root, padding=20)
        self.main.pack(side=RIGHT, fill=BOTH, expand=True)

        ttk.Label(
            self.main,
            text="Bienvenido a HUB Hogar",
            font=("Helvetica", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self.main,
            text="Centro de control familiar",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(0, 20))

        # Tarjeta Finanzas

        card1 = ttk.Labelframe(self.main, text="Finanzas", padding=15)
        card1.pack(fill=X, pady=10)

        ttk.Label(
            card1,
            text=f"Balance actual: ${resumen['balance']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Ingresos: ${resumen['ingresos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Gastos: ${resumen['gastos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Movimientos: {resumen['movimientos']}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Último movimiento: {resumen['ultimo_concepto']}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Monto: ${resumen['ultimo_monto']:,.2f}"
        ).pack(anchor="w")

        # Tarjeta Respaldos
        card2 = ttk.Labelframe(self.main, text="Respaldos", padding=15)
        card2.pack(fill=X, pady=10)

        ttk.Label(
            card2,
            text=f"Respaldos realizados: {respaldos['total_respaldos']}"
        ).pack(anchor="w")

        ttk.Label(
            card2,
            text=f"Último respaldo: {respaldos['ultimo_respaldo']}"
        ).pack(anchor="w")

        # Botones
        botones = ttk.Frame(self.main)
        botones.pack(pady=20)

        ttk.Button(
            botones,
            text="📄 Generar Reporte Mensual",
            bootstyle="info",
            command=self.generar_reporte_mensual
        ).pack(side=LEFT, padx=10)

        ttk.Button(
            botones,
            text="Abrir AFI",
            bootstyle="success",
            command=self.abrir_afi
        ).pack(side=LEFT, padx=10)

        ttk.Button(
            botones,
            text="Abrir ADP",
            bootstyle="info",
            command=self.abrir_adp
        ).pack(side=LEFT, padx=10)

        self.mostrar_dashboard()

    def abrir_afi(self):

        subprocess.Popen(
            [
                "/Users/luisbonilla/Documents/Python/Activos/AFI_V2/venv/bin/python",
                "app.py"
            ],
            cwd="/Users/luisbonilla/Documents/Python/Activos/AFI_V2"
        )

    def abrir_adp(self):

        subprocess.Popen(
            [
                "/Users/luisbonilla/Documents/Python/Activos/ADP/venv/bin/python",
                "app.py"
            ],
            cwd="/Users/luisbonilla/Documents/Python/Activos/ADP"
        )

    def limpiar_contenido(self):

        for widget in self.main.winfo_children():
            widget.destroy()

    def mostrar_hogar(self):

        self.limpiar_contenido()

        vista = HogarView(self.main)

        vista.frame.pack(
            fill="both",
            expand=True
        )

    def mostrar_dashboard(self):

        self.limpiar_contenido()

        ttk.Label(
            self.main,
            text="Bienvenido a HUB Hogar",
            font=("Helvetica", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self.main,
            text="Centro de control familiar",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(0, 20))

        resumen = obtener_resumen_financiero()
        respaldos = obtener_resumen_respaldos()
        hogar = obtener_dashboard_hogar()
        
        disponible = (
            resumen["balance"]
            - hogar["total_mes"]
        )


        card0 = ttk.Labelframe(
            self.main,
            text="Disponible después de compromisos",
            padding=15
        )

        card0.pack(
            fill=X,
            pady=10
        )

        ttk.Label(
            card0,
            text=f"${disponible:,.2f}",
            font=("Helvetica", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            card0,
            text=(
                f"Balance: ${resumen['balance']:,.2f}  |  "
                f"Compromisos del mes: ${hogar['total_mes']:,.2f}"
            )
        ).pack(anchor="w")

        card3 = ttk.Labelframe(
            self.main,
            text="Obligaciones",
            padding=15
        )

        card3.pack(
            fill=X,
            pady=10
        )

        ttk.Label(
            card3,
            text=f"Obligaciones activas: {hogar['activas']}"
        ).pack(anchor="w")

        ttk.Label(
            card3,
            text=f"Compromisos este mes: {hogar['compromisos_mes']}"
        ).pack(anchor="w")

        ttk.Label(
            card3,
            text=f"Total este mes: ${hogar['total_mes']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card3,
            text=f"Total registrado: ${hogar['total']:,.2f}"
        ).pack(anchor="w")


        card1 = ttk.Labelframe(
            self.main,
            text="Finanzas",
            padding=15
        )
        card1.pack(fill=X, pady=10)

        ttk.Label(
            card1,
            text=f"Balance actual: ${resumen['balance']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Ingresos: ${resumen['ingresos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Gastos: ${resumen['gastos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Movimientos: {resumen['movimientos']}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Último movimiento: {resumen['ultimo_concepto']}"
        ).pack(anchor="w")

        ttk.Label(
            card1,
            text=f"Monto: ${resumen['ultimo_monto']:,.2f}"
        ).pack(anchor="w")

        card2 = ttk.Labelframe(
            self.main,
            text="Respaldos",
            padding=15
        )
        card2.pack(fill=X, pady=10)

        ttk.Label(
            card2,
            text=f"Respaldos realizados: {respaldos['total_respaldos']}"
        ).pack(anchor="w")

        ttk.Label(
            card2,
            text=f"Último respaldo: {respaldos['ultimo_respaldo']}"
        ).pack(anchor="w")


    def mostrar_finanzas(self):

        self.limpiar_contenido()

        resumen = obtener_resumen_financiero()

        pagos_mes = obtener_obligaciones_mes_actual()

        hogar = obtener_dashboard_hogar()

        disponible_real = (
            resumen["balance"]
            - hogar["total_mes"]
        )

        if disponible_real >= 0:
            diagnostico = "🟢 Saludable"
        else:
            diagnostico = "🔴 Comprometido"

        ttk.Label(
            self.main,
            text="💰 Finanzas",
            font=("Helvetica", 20, "bold")
        ).pack(anchor="w")

        ttk.Button(
            self.main,
            text="📄 Generar Reporte Mensual",
            bootstyle="info",
            command=self.generar_reporte_mensual
        ).pack(pady=10)

        ttk.Label(
            self.main,
            text="Resumen financiero de AFI",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(0, 20))

        card = ttk.Labelframe(
            self.main,
            text="Estado Financiero",
            padding=15
        )
        card.pack(fill=X, pady=10)

        ttk.Label(
            card,
            text=f"Balance actual: ${resumen['balance']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Ingresos: ${resumen['ingresos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Gastos: ${resumen['gastos']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Movimientos: {resumen['movimientos']}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Último movimiento: {resumen['ultimo_concepto']}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Monto: ${resumen['ultimo_monto']:,.2f}"
        ).pack(anchor="w")

        ttk.Separator(
            card
        ).pack(
            fill=X,
            pady=10
        )

        ttk.Label(
            card,
            text=f"Compromisos del mes: ${hogar['total_mes']:,.2f}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Obligaciones pendientes: {hogar['compromisos_mes']}"
        ).pack(anchor="w")

        color_disponible = "green"

        if disponible_real < 0:
            color_disponible = "red"
 
        ttk.Label(
            card,
            text=f"Disponible real: ${disponible_real:,.2f}",
            font=("Helvetica", 11, "bold"),
            foreground=color_disponible
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Diagnóstico del mes: {diagnostico}",
            font=("Helvetica", 11, "bold")
        ).pack(anchor="w")

        card_pagos = ttk.Labelframe(
            self.main,
            text="Pagos del Mes",
            padding=15
        )

        card_pagos.pack(
            fill=X,
            pady=10
        )

        ttk.Label(
            card_pagos,
            text=f"{'Fecha':<12} {'Obligación':<30} {'Importe'}",
            font=("Courier", 10, "bold")
        ).pack(anchor="w")

        ttk.Separator(card_pagos).pack(
            fill=X,
            pady=5
        )

        total_mes = 0

        for pago in pagos_mes:

            total_mes += pago["monto"]

            fecha = pago["fecha"][8:10] + "/" + pago["fecha"][5:7] + "/" + pago["fecha"][0:4]

            ttk.Label(
                card_pagos,
                text=f"{fecha:<12} {pago['nombre']:<30} ${pago['monto']:>10,.2f}",
                font=("Courier", 10)
            ).pack(anchor="w")


        ttk.Button(
            self.main,
            text="Abrir AFI",
            bootstyle="success",
            command=self.abrir_afi
        ).pack(pady=20)

        ttk.Separator(card_pagos).pack(
            fill=X,
            pady=5
        )

        ttk.Label(
            card_pagos,
            text=f"TOTAL DEL MES: ${total_mes:,.2f}",
            font=("Helvetica", 11, "bold")
        ).pack(anchor="e", pady=(5,0))

    def generar_reporte_mensual(self):

        from pathlib import Path

        carpeta_reportes = Path("reportes")

        carpeta_reportes.mkdir(
            exist_ok=True
        )

        from datetime import datetime

        hoy = datetime.now()

        nombre_archivo = (
            f"{hoy.year}_{hoy.month:02d}_reporte.md"
        )

        ruta_archivo = (
            carpeta_reportes / nombre_archivo
        )

        resumen = obtener_resumen_financiero()

        hogar = obtener_dashboard_hogar()

        pagos_mes = obtener_obligaciones_mes_actual()

        movimientos = obtener_movimientos_mes_actual()

        categorias = {}

        for fecha, concepto, categoria, tipo, monto in movimientos:

            if tipo == "Gasto":

                categorias[categoria] = (
                    categorias.get(categoria, 0)
                    + monto
                )

        disponible_real = (
            resumen["balance"]
            - hogar["total_mes"]
        )

        if disponible_real >= 0:
            diagnostico = "SALUDABLE"
        else:
            diagnostico = "COMPROMETIDO"

        with open(
            ruta_archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                "# REPORTE FINANCIERO MENSUAL\n\n"
            )

            archivo.write(
                f"Periodo: {hoy.month:02d}/{hoy.year}\n\n"
            )

            archivo.write(
                "## ESTADO FINANCIERO\n\n"
            )

            archivo.write(
                f"- Balance actual: ${resumen['balance']:,.2f}\n"
            )

            archivo.write(
                f"- Ingresos: ${resumen['ingresos']:,.2f}\n"
            )

            archivo.write(
                f"- Gastos: ${resumen['gastos']:,.2f}\n"
            )

            archivo.write(
                f"- Movimientos registrados: {resumen['movimientos']}\n\n"
            )

            archivo.write(
                "## GASTOS POR CATEGORIA\n\n"
            )

            for categoria, total in sorted(
                categorias.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                archivo.write(
                    f"- {categoria}: ${total:,.2f}\n"
                )

            archivo.write("\n")


            archivo.write(
                "## MOVIMIENTOS DEL MES\n\n"
            )

            for fecha, concepto, categoria, tipo, monto in movimientos:

                archivo.write(
                    f"### {concepto}\n\n"
                )

                archivo.write(
                    f"- Fecha: {fecha}\n"
                )

                archivo.write(
                    f"- Categoría: {categoria}\n"
                )

                if tipo == "Ingreso":
                    tipo_texto = "🟢 Ingreso"
                else:
                    tipo_texto = "🔴 Gasto"

                archivo.write(
                    f"- Tipo: {tipo_texto}\n"
                )

                archivo.write(
                    f"- Monto: ${monto:,.2f}\n\n"
                )

            archivo.write(
                "## OBLIGACIONES DEL MES\n\n"
            )

            for pago in pagos_mes:

                fecha = (
                    pago["fecha"][8:10]
                    + "/"
                    + pago["fecha"][5:7]
                    + "/"
                    + pago["fecha"][0:4]
                )

                archivo.write(
                    f"- {fecha} | "
                    f"{pago['nombre']} | "
                    f"${pago['monto']:,.2f}\n"
                )

            archivo.write("\n")

            archivo.write(
                "## ANALISIS DEL MES\n\n"
            )

            archivo.write(
                "### Resumen\n\n"
            )

            archivo.write(
                f"- Compromisos del mes: ${hogar['total_mes']:,.2f}\n"
            )

            archivo.write(
                f"- Obligaciones pendientes: {hogar['compromisos_mes']}\n"
            )

            archivo.write(
                f"- Disponible real: ${disponible_real:,.2f}\n\n"
            )

            archivo.write(
                "### Diagnóstico\n\n"
            )

            if disponible_real >= 0:

                archivo.write(
                    "🟢 SALUDABLE\n\n"
                )

                archivo.write(
                    (
                        f"Después de cubrir todas las obligaciones del mes "
                        f"permanecerían disponibles "
                        f"${disponible_real:,.2f}.\n\n"
                    )
                )

                archivo.write(
                    (
                        "Existe margen para ahorro, inversión "
                        "o amortización de deuda.\n\n"
                    )
                )

            else:

                faltante = abs(disponible_real)

                archivo.write(
                    "🔴 COMPROMETIDO\n\n"
                )

                archivo.write(
                    (
                        f"Los compromisos registrados para el mes "
                        f"superan el balance disponible por "
                        f"${faltante:,.2f}.\n\n"
                    )
                )

                archivo.write(
                    (
                        "Se recomienda priorizar obligaciones esenciales "
                        "y revisar gastos variables antes de asumir "
                        "nuevos compromisos.\n\n"
                    )
                )


    def mostrar_respaldos(self):

        self.limpiar_contenido()

        respaldos = obtener_resumen_respaldos()

        ttk.Label(
            self.main,
            text="☁️ Respaldos",
            font=("Helvetica", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self.main,
            text="Estado actual de ADP",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(0, 20))

        card = ttk.Labelframe(
            self.main,
            text="Protección de Datos",
            padding=15
        )
        card.pack(fill=X, pady=10)

        ttk.Label(
            card,
            text=f"Respaldos realizados: {respaldos['total_respaldos']}"
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=f"Último respaldo: {respaldos['ultimo_respaldo']}"
        ).pack(anchor="w")

        ttk.Separator(card).pack(
            fill=X,
            pady=10
        )

        ttk.Label(
            card,
            text="Carpetas respaldadas:",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w")

        for carpeta in respaldos.get("carpetas", []):
            ttk.Label(
                card,
                text=f"✅ {carpeta}"
            ).pack(anchor="w")

        ttk.Button(
            self.main,
            text="Abrir ADP",
            bootstyle="info",
            command=self.abrir_adp
        ).pack(pady=20)

app = ttk.Window(themename="flatly")
HubHogar(app)
app.mainloop()

