import tkinter as tk
from tkinter import messagebox
from core.logica_inventario import crear_producto


class ProductoForm:

    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success_callback = on_success_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Producto")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        # Modal
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus()

        self.window.protocol("WM_DELETE_WINDOW", self._cerrar_formulario)

        self._build_form()

    def _build_form(self):

        tk.Label(self.window, text="Código").pack(pady=5)
        self.codigo_entry = tk.Entry(self.window)
        self.codigo_entry.pack(pady=5)

        tk.Label(self.window, text="Nombre").pack(pady=5)
        self.nombre_entry = tk.Entry(self.window)
        self.nombre_entry.pack(pady=5)

        tk.Label(self.window, text="Precio (COP)").pack(pady=5)
        self.precio_entry = tk.Entry(self.window)
        self.precio_entry.pack(pady=5)

        tk.Label(self.window, text="Stock Inicial").pack(pady=5)
        self.stock_entry = tk.Entry(self.window)
        self.stock_entry.pack(pady=5)

        tk.Label(self.window, text="Stock Mínimo").pack(pady=5)
        self.minimo_entry = tk.Entry(self.window)
        self.minimo_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="Guardar",
            command=self._guardar_producto
        ).pack(pady=15)

    def _guardar_producto(self):

        try:
            codigo = self.codigo_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            precio = int(self.precio_entry.get())
            stock = int(self.stock_entry.get())
            minimo = int(self.minimo_entry.get())

            ok, mensaje = crear_producto(
                codigo,
                nombre,
                precio,
                stock,
                minimo
            )

            if not ok:
                messagebox.showerror("Error", mensaje)
                return

            messagebox.showinfo("Éxito", mensaje)

            self.on_success_callback()
            self.window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Precio, stock y mínimo deben ser números enteros"
            )

    def _cerrar_formulario(self):
        self.window.destroy()