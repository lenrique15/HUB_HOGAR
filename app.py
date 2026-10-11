import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
from modules.afi_connector import obtener_resumen_financiero



class HubHogar:

    def __init__(self, root):
        self.root = root

        resumen = obtener_resumen_financiero()

        root.title("HUB Hogar 0.1 ALPHA")

        width = 1000
        height = 600

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
            text="Dashboard",
            bootstyle="primary"
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="Finanzas"
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="Respaldos"
        ).pack(fill=X, pady=5)

        ttk.Button(
            sidebar,
            text="Hogar"
        ).pack(fill=X, pady=5)

        # Área principal
        main = ttk.Frame(root, padding=20)
        main.pack(side=RIGHT, fill=BOTH, expand=True)

        ttk.Label(
            main,
            text="Bienvenido a HUB Hogar",
            font=("Helvetica", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Centro de control familiar",
            font=("Helvetica", 11)
        ).pack(anchor="w", pady=(0, 20))

        # Tarjeta Finanzas
        card1 = ttk.Labelframe(main, text="Finanzas", padding=15)
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
        card2 = ttk.Labelframe(main, text="Respaldos", padding=15)
        card2.pack(fill=X, pady=10)

        ttk.Label(
            card2,
            text="ADP conectado próximamente"
        ).pack(anchor="w")

        # Botones
        botones = ttk.Frame(main)
        botones.pack(pady=20)

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

app = ttk.Window(themename="flatly")
HubHogar(app)
app.mainloop()