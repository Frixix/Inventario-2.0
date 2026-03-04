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
        self.root.geometry("1100x750")
        self.root.resizable(False, False)

        self._configurar_estilos()
        self._build_layout()
        self._cargar_productos()

    # =========================
    # ESTILOS
    # =========================
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Fuente general
        style.configure(".", font=("Segoe UI", 10))

        # Botones
        style.configure("TButton", padding=6)

        # Tabla
        style.configure("Treeview", rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # =========================
    # INTERFAZ
    # =========================
    def _build_layout(self):

        # ===== HEADER SUPERIOR =====
        header = tk.Frame(self.root, bg="#1f2937", height=60)
        header.pack(fill="x")

        titulo = tk.Label(
            header,
            text="Sistema de Inventario",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 16, "bold")
        )
        titulo.pack(pady=15)

        # ===== TABLA =====
        columnas = ("ID", "Código", "Nombre", "Precio", "Stock", "Mínimo")

        frame_tabla = ttk.Frame(self.root)
        frame_tabla.pack(pady=20)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=140, anchor="center")

        # Ajuste fino de columnas
        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Código", width=120, anchor="center")
        self.tabla.column("Nombre", width=220, anchor="w")
        self.tabla.column("Precio", width=120, anchor="center")
        self.tabla.column("Stock", width=100, anchor="center")
        self.tabla.column("Mínimo", width=100, anchor="center")

        self.tabla.pack()

        # ===== SEPARADOR =====
        separador = ttk.Separator(self.root, orient="horizontal")
        separador.pack(fill="x", pady=10)

        # ===== BOTONES =====
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=10)

        self.btn_refrescar = ttk.Button(
            frame_botones,
            text="Refrescar",
            width=20,
            command=self._cargar_productos
        )
        self.btn_refrescar.grid(row=0, column=0, padx=10)

        self.btn_registrar = ttk.Button(
            frame_botones,
            text="Registrar Producto",
            width=20,
            command=self._abrir_formulario_producto
        )
        self.btn_registrar.grid(row=0, column=1, padx=10)

        self.btn_entrada = ttk.Button(
            frame_botones,
            text="Entrada de Inventario",
            width=20,
            command=self._abrir_formulario_entrada
        )
        self.btn_entrada.grid(row=0, column=2, padx=10)

        self.btn_salida = ttk.Button(
            frame_botones,
            text="Salida de Inventario",
            width=20,
            command=self._abrir_formulario_salida
        )
        self.btn_salida.grid(row=0, column=3, padx=10)

        self.btn_ver_salidas = ttk.Button(
            frame_botones,
            text="Ver Salidas",
            width=20,
            command=self._abrir_salidas_view
        )
        self.btn_ver_salidas.grid(row=1, column=0, columnspan=2, pady=10)

    # =========================
    # CARGAR PRODUCTOS
    # =========================
    def _cargar_productos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = listar_productos()

        for p in productos:
            id_, codigo, nombre, precio, stock, minimo, activo = p

            self.tabla.insert(
                "",
                tk.END,
                values=(id_, codigo, nombre, precio, stock, minimo)
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
    # FORMULARIOS
    # =========================
    def _abrir_formulario_producto(self):
        self._deshabilitar_botones()
        form = ProductoForm(self.root, self._on_datos_modificados)
        self.root.wait_window(form.window)
        self._habilitar_botones()

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

    def _abrir_salidas_view(self):
        SalidasView(self.root)

    # =========================
    # CALLBACK
    # =========================
    def _on_datos_modificados(self):
        self._cargar_productos()

    # =========================
    # ESTADO BOTONES
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

    def run(self):
        self.root.mainloop()