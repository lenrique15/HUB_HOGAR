import ttkbootstrap as ttk

from hogar.view import HogarView

app = ttk.Window(themename="flatly")

vista = HogarView(app)

vista.frame.pack(
    fill="both",
    expand=True
)

app.mainloop()
