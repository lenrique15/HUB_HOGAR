import ttkbootstrap as ttk

from hogar.service import obtener_obligaciones


class HogarView:

    def __init__(self, parent):

        self.frame = ttk.Frame(parent)

        ttk.Label(
            self.frame,
            text="🏡 Obligaciones del Hogar",
            font=("Helvetica", 18, "bold")
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        self.lista = ttk.Treeview(
            self.frame,
            columns=(
                "nombre",
                "categoria",
                "monto",
                "frecuencia",
                "fecha"
            ),
            show="headings",
            height=10
        )

        self.lista.heading(
            "nombre",
            text="Nombre"
        )

        self.lista.heading(
            "categoria",
            text="Categoría"
        )

        self.lista.heading(
            "monto",
            text="Monto"
        )

        self.lista.heading(
            "frecuencia",
            text="Frecuencia"
        )

        self.lista.heading(
            "fecha",
            text="Próxima Fecha"
        )

        self.lista.pack(
            fill="both",
            expand=True
        )

        self.cargar_datos()

    def cargar_datos(self):

        for fila in obtener_obligaciones():

            self.lista.insert(
                "",
                "end",
                values=(
                    fila[1],
                    fila[2],
                    f"${fila[3]:,.2f}",
                    fila[4],
                    fila[5]
                )
            )