import tkinter as tk
from tkinter import ttk, messagebox
from core.logica_inventario import listar_productos
from ui.producto_form import ProductoForm
from ui.entrada_form import EntradaForm
from ui.salida_form import SalidaForm
from ui.salidas_view import SalidasView


class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Inventario")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        self._build_layout()
        self._cargar_productos()

    # =========================
    # CONSTRUCCIÓN INTERFAZ
    # =========================
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

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=15)

        self.btn_refrescar = tk.Button(
            frame_botones,
            text="Refrescar",
            width=20,
            command=self._cargar_productos
        )
        self.btn_refrescar.grid(row=0, column=0, padx=10)

        self.btn_registrar = tk.Button(
            frame_botones,
            text="Registrar Producto",
            width=20,
            command=self._abrir_formulario_producto
        )
        self.btn_registrar.grid(row=0, column=1, padx=10)

        self.btn_entrada = tk.Button(
            frame_botones,
            text="Entrada de Inventario",
            width=20,
            command=self._abrir_formulario_entrada
        )
        self.btn_entrada.grid(row=0, column=2, padx=10)

        self.btn_salida = tk.Button(
            frame_botones,
            text="Salida de Inventario",
            width=20,
            command=self._abrir_formulario_salida
        )
        self.btn_salida.grid(row=0, column=3, padx=10)

        self.btn_ver_salidas = tk.Button(
            frame_botones,
            text="Ver Salidas",
            width=20,
            command=self._abrir_salidas_view
        )
        self.btn_ver_salidas.grid(row=1, column=0, columnspan=2, pady=10)

    # =========================
    # VER SALIDAS
    # =========================
    def _abrir_salidas_view(self):
        SalidasView(self.root)

    # =========================
    # CARGA DE DATOS
    # =========================
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

    # =========================
    # UTILIDADES
    # =========================
    def _obtener_producto_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            return None

        item = self.tabla.item(seleccion[0])
        valores = item["values"]

        return valores[0]

    # =========================
    # FORMULARIO PRODUCTO
    # =========================
    def _abrir_formulario_producto(self):

        self._deshabilitar_botones()

        form = ProductoForm(self.root, self._on_datos_modificados)

        self.root.wait_window(form.window)

        self._habilitar_botones()

    # =========================
    # FORMULARIO ENTRADA
    # =========================
    def _abrir_formulario_entrada(self):

        producto_id = self._obtener_producto_seleccionado()

        if producto_id is None:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar un producto primero."
            )
            return

        self._deshabilitar_botones()

        form = EntradaForm(
            self.root,
            producto_id,
            self._on_datos_modificados
        )

        self.root.wait_window(form.window)

        self._habilitar_botones()

    # =========================
    # FORMULARIO SALIDA
    # =========================
    def _abrir_formulario_salida(self):

        producto_id = self._obtener_producto_seleccionado()

        if producto_id is None:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar un producto primero."
            )
            return

        self._deshabilitar_botones()

        form = SalidaForm(
            self.root,
            producto_id,
            self._on_datos_modificados
        )

        self.root.wait_window(form.window)

        self._habilitar_botones()

    # =========================
    # CALLBACK GENERAL
    # =========================
    def _on_datos_modificados(self):
        self._cargar_productos()

    # =========================
    # CONTROL DE ESTADO BOTONES
    # =========================
    def _deshabilitar_botones(self):
        self.btn_refrescar.config(state="disabled")
        self.btn_registrar.config(state="disabled")
        self.btn_entrada.config(state="disabled")
        self.btn_salida.config(state="disabled")

    def _habilitar_botones(self):
        self.btn_refrescar.config(state="normal")
        self.btn_registrar.config(state="normal")
        self.btn_entrada.config(state="normal")
        self.btn_salida.config(state="normal")

    # =========================
    # RUN
    # =========================
    def run(self):
        self.root.mainloop()