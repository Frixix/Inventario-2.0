import tkinter as tk
from tkinter import ttk
from core.database import obtener_salidas


class SalidasView:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("SALIDAS")
        self.window.geometry("750x400")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._build_layout()
        self._cargar_datos()

    def _build_layout(self):

        tk.Label(
            self.window,
            text="SALIDAS",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        columnas = ("Código", "Artículo", "Fecha", "Cantidad", "Motivo")

        self.tabla = ttk.Treeview(
            self.window,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=140, anchor="center")

        self.tabla.pack(pady=10)

    def _cargar_datos(self):

        salidas = obtener_salidas()

        for fila in salidas:
            codigo, nombre, fecha, cantidad, motivo = fila

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    codigo,
                    nombre,
                    fecha,
                    abs(cantidad),  # mostramos positivo
                    motivo if motivo else ""
                )
            )