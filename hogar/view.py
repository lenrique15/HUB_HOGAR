import ttkbootstrap as ttk

from hogar.service import (
    obtener_obligaciones,
    agregar_obligacion,
    actualizar_obligacion,
    desactivar_obligacion as desactivar_bd,
    obtener_resumen_obligaciones,
    obtener_resumen_mes_actual
)



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


        resumen = obtener_resumen_obligaciones()

        resumen_mes = obtener_resumen_mes_actual()

        ttk.Label(
            self.frame,
            text=f"Obligaciones activas: {resumen['total_registros']}"
        ).pack(anchor="w")

        ttk.Label(
            self.frame,
            text=f"Total registrado: ${resumen['total_monto']:,.2f}"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )


        ttk.Label(
            self.frame,
            text=f"Compromisos este mes: {resumen_mes['cantidad']}"
        ).pack(anchor="w")

        ttk.Label(
            self.frame,
            text=f"Total este mes: ${resumen_mes['total']:,.2f}"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        barra_botones = ttk.Frame(
            self.frame
        )

        barra_botones.pack(
            anchor="w",
            pady=(0, 15)
        )

        ttk.Button(
            barra_botones,
            text="➕ Nueva Obligación",
            bootstyle="success",
            command=self.nueva_obligacion
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            barra_botones,
            text="✏️ Editar",
            bootstyle="warning",
            command=self.editar_obligacion
        ).pack(
            side="left"
        )

        ttk.Button(
            barra_botones,
            text="🗑️ Desactivar",
            bootstyle="danger",
            command=self.desactivar_obligacion
        ).pack(
            side="left",
            padx=(10, 0)
        )

        self.lista = ttk.Treeview(
            self.frame,
            columns=(
                "id",
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
            "id",
            text="ID"
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

        self.lista.column(
            "nombre",
            width=250
        )

        self.lista.column(
            "categoria",
            width=180
        )

        self.lista.column(
            "monto",
            width=120
        )

        self.lista.column(
            "frecuencia",
            width=150
        )

        self.lista.column(
            "fecha",
            width=150
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
                    fila[0],
                    fila[1],
                    fila[2],
                    f"${fila[3]:,.2f}",
                    fila[4],
                    fila[5]
                )
            )
    def nueva_obligacion(self):

        ventana = ttk.Toplevel()

        ventana.title("Nueva Obligación")
        ventana.geometry("400x400")

        ttk.Label(
            ventana,
            text="Nombre"
        ).pack(pady=(10, 0))

        entry_nombre = ttk.Entry(
            ventana,
            width=30
        )
        entry_nombre.pack()

        ttk.Label(
            ventana,
            text="Categoría"
        ).pack(pady=(10, 0))

        combo_categoria = ttk.Combobox(
            ventana,
            values=[
                "Servicio",
                "Suscripción",
                "Hogar",
                "Personal",
                "Otro"
            ]
        )
        combo_categoria.pack()

        ttk.Label(
            ventana,
            text="Monto"
        ).pack(pady=(10, 0))

        entry_monto = ttk.Entry(
            ventana,
            width=30
        )
        entry_monto.pack()

        ttk.Label(
            ventana,
            text="Frecuencia"
        ).pack(pady=(10, 0))

        combo_frecuencia = ttk.Combobox(
            ventana,
            values=[
                "Semanal",
                "Quincenal",
                "Mensual",
                "Bimestral",
                "Trimestral",
                "Semestral",
                "Anual",
                "A demanda"
            ]
        )
        combo_frecuencia.pack()

        ttk.Label(
            ventana,
            text="Próxima Fecha (AAAA-MM-DD)"
        ).pack(pady=(10, 0))

        entry_fecha = ttk.Entry(
            ventana,
            width=30
        )
        entry_fecha.pack()

        def guardar():

            agregar_obligacion(
                entry_nombre.get(),
                combo_categoria.get(),
                float(entry_monto.get()),
                combo_frecuencia.get(),
                entry_fecha.get()
            )

            ventana.destroy()

            for item in self.lista.get_children():
                self.lista.delete(item)

            self.cargar_datos()

        ttk.Button(
            ventana,
            text="Guardar",
            bootstyle="success",
            command=guardar
        ).pack(
            pady=20
        )

    def editar_obligacion(self):

        seleccion = self.lista.selection()

        if not seleccion:
            print("Seleccione un registro")
            return

        valores = self.lista.item(
            seleccion[0]
        )["values"]

        obligacion_id = valores[0]

        ventana = ttk.Toplevel()

        ventana.title("Editar Obligación")
        ventana.geometry("400x400")

        ttk.Label(
            ventana,
            text="Nombre"
        ).pack(pady=(10, 0))

        entry_nombre = ttk.Entry(
            ventana,
            width=30
        )
        entry_nombre.pack()
        entry_nombre.insert(0, valores[1])

        ttk.Label(
            ventana,
            text="Categoría"
        ).pack(pady=(10, 0))

        combo_categoria = ttk.Combobox(
            ventana,
            values=[
                "Servicio",
                "Suscripción",
                "Hogar",
                "Personal",
                "Otro"
            ]
        )
        combo_categoria.pack()
        combo_categoria.set(valores[2])

        ttk.Label(
            ventana,
            text="Monto"
        ).pack(pady=(10, 0))

        entry_monto = ttk.Entry(
            ventana,
            width=30
        )
        entry_monto.pack()
        entry_monto.insert(
            0,
            str(valores[3]).replace("$", "").replace(",", "")
        )

        ttk.Label(
            ventana,
            text="Frecuencia"
        ).pack(pady=(10, 0))

        combo_frecuencia = ttk.Combobox(
            ventana,
            values=[
                "Semanal",
                "Quincenal",
                "Mensual",
                "Bimestral",
                "Trimestral",
                "Semestral",
                "Anual",
                "A demanda"
            ]
        )
        combo_frecuencia.pack()
        combo_frecuencia.set(valores[4])

        ttk.Label(
            ventana,
            text="Próxima Fecha"
        ).pack(pady=(10, 0))

        entry_fecha = ttk.Entry(
            ventana,
            width=30
        )
        entry_fecha.pack()
        entry_fecha.insert(0, valores[5])

        def guardar_cambios():

            actualizar_obligacion(
                obligacion_id,
                entry_nombre.get(),
                combo_categoria.get(),
                float(entry_monto.get()),
                combo_frecuencia.get(),
                entry_fecha.get()
            )

            ventana.destroy()

            for item in self.lista.get_children():
                self.lista.delete(item)

            self.cargar_datos()

        ttk.Button(
            ventana,
            text="Guardar cambios",
            bootstyle="warning",
            command=guardar_cambios
        ).pack(
            pady=20
        )

    def desactivar_obligacion(self):

        seleccion = self.lista.selection()

        if not seleccion:
            print("Seleccione un registro")
            return

        valores = self.lista.item(
            seleccion[0]
        )["values"]

        obligacion_id = valores[0]

        desactivar_bd(
            obligacion_id
        )

        for item in self.lista.get_children():
            self.lista.delete(item)

        self.cargar_datos()