import tkinter as tk
from tkinter import messagebox
from core.logica_inventario import salida_producto


class SalidaForm:

    def __init__(self, parent, producto_id, callback):

        self.producto_id = producto_id
        self.callback = callback

        self.window = tk.Toplevel(parent)
        self.window.title("Salida de Inventario")
        self.window.geometry("350x250")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._build_layout()

    def _build_layout(self):

        tk.Label(self.window, text="Cantidad a retirar:").pack(pady=10)

        self.entry_cantidad = tk.Entry(self.window)
        self.entry_cantidad.pack(pady=5)

        tk.Label(self.window, text="Cliente:").pack(pady=10)

        self.entry_cliente = tk.Entry(self.window)
        self.entry_cliente.pack(pady=5)

        tk.Button(
            self.window,
            text="Confirmar",
            command=self._procesar_salida
        ).pack(pady=15)

    def _procesar_salida(self):

        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        cliente = self.entry_cliente.get().strip()

        if not cliente:
            messagebox.showerror("Error", "Debe indicar el cliente.")
            return

        ok, mensaje = salida_producto(
            self.producto_id,
            cantidad,
            cliente
        )

        if not ok:
            messagebox.showerror("Error", mensaje)
            return

        messagebox.showinfo("Éxito", mensaje)

        if self.callback:
            self.callback()

        self.window.destroy()