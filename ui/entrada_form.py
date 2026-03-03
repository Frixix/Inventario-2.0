import tkinter as tk
from tkinter import messagebox
from core.logica_inventario import entrada_producto


class EntradaForm:

    def __init__(self, parent, producto_id, callback):

        self.producto_id = producto_id
        self.callback = callback

        self.window = tk.Toplevel(parent)
        self.window.title("Entrada de Inventario")
        self.window.geometry("350x250")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._build_layout()

    def _build_layout(self):

        tk.Label(
            self.window,
            text="Cantidad a ingresar:"
        ).pack(pady=10)

        self.entry_cantidad = tk.Entry(self.window)
        self.entry_cantidad.pack(pady=5)

        tk.Label(
            self.window,
            text="Motivo:"
        ).pack(pady=10)

        self.entry_motivo = tk.Entry(self.window)
        self.entry_motivo.pack(pady=5)

        tk.Button(
            self.window,
            text="Confirmar",
            command=self._procesar_entrada
        ).pack(pady=15)

    def _procesar_entrada(self):

        try:
            cantidad = int(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        motivo = self.entry_motivo.get().strip()

        if not motivo:
            messagebox.showerror("Error", "Debe indicar un motivo.")
            return

        ok, mensaje = entrada_producto(
            self.producto_id,
            cantidad,
            motivo
        )

        if not ok:
            messagebox.showerror("Error", mensaje)
            return

        messagebox.showinfo("Éxito", mensaje)

        if self.callback:
            self.callback()

        self.window.destroy()