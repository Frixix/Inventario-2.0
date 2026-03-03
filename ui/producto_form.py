import tkinter as tk
from tkinter import messagebox
from core.logica_inventario import crear_producto


class ProductoForm:

    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success_callback = on_success_callback

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Producto")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self._build_form()

    def _build_form(self):

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
            nombre = self.nombre_entry.get().strip()
            precio = int(self.precio_entry.get())
            stock = int(self.stock_entry.get())
            minimo = int(self.minimo_entry.get())

            ok, mensaje = crear_producto(nombre, precio, stock, minimo)

            if not ok:
                messagebox.showerror("Error", mensaje)
                return

            messagebox.showinfo("Éxito", "Producto registrado correctamente")

            self.on_success_callback()
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Precio, stock y mínimo deben ser números enteros")