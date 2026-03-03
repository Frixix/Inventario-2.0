import tkinter as tk
from tkinter import ttk
from core.logica_inventario import listar_productos
from ui.producto_form import ProductoForm


class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Inventario")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self._build_layout()
        self._cargar_productos()

    def _build_layout(self):

        titulo = tk.Label(
            self.root,
            text="Sistema de Inventario",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        # =========================
        # TABLA DE PRODUCTOS
        # =========================

        columnas = ("ID", "Nombre", "Precio", "Stock", "Mínimo")

        self.tabla = ttk.Treeview(
            self.root,
            columns=columnas,
            show="headings",
            height=15
        )

        # Configuración específica por columna
        self.tabla.heading("ID", text="ID")
        self.tabla.column("ID", width=60, anchor="center")

        self.tabla.heading("Nombre", text="Nombre del Producto")
        self.tabla.column("Nombre", width=250, anchor="w")

        self.tabla.heading("Precio", text="Precio (COP)")
        self.tabla.column("Precio", width=120, anchor="center")

        self.tabla.heading("Stock", text="Stock Actual")
        self.tabla.column("Stock", width=120, anchor="center")

        self.tabla.heading("Mínimo", text="Stock Mínimo")
        self.tabla.column("Mínimo", width=120, anchor="center")

        self.tabla.pack(pady=10)

        # =========================
        # BOTONES
        # =========================

        boton_refrescar = tk.Button(
            self.root,
            text="Refrescar",
            command=self._cargar_productos
        )
        boton_refrescar.pack(pady=5)

        # Guardamos como atributo
        self.btn_registrar = tk.Button(
            self.root,
            text="Registrar Producto",
            command=self._abrir_formulario_producto
        )

        self.btn_registrar.pack(pady=5)

    def _cargar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = listar_productos()

        for p in productos:
            id_, nombre, precio, stock, minimo, activo = p
            self.tabla.insert(
                "",
                tk.END,
                values=(id_, nombre, precio, stock, minimo)
            )

    def _abrir_formulario_producto(self):

        # Deshabilitamos botón
        self.btn_registrar.config(state="disabled")

        form = ProductoForm(self.root, self._on_producto_creado)

        # Esperamos a que se cierre la ventana
        self.root.wait_window(form.window)

        # Se vuelve a habilitar SIEMPRE
        self.btn_registrar.config(state="normal")

    def _on_producto_creado(self):
        self._cargar_productos()

    def run(self):
        self.root.mainloop()