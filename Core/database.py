import sqlite3
from datetime import datetime

DB_NAME = "inventario.db"


# ======================================================
# CONEXIÓN
# ======================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ======================================================
# CREAR TABLAS (Migración limpia)
# ======================================================

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # ----------------------
    # TABLA PRODUCTOS
    # ----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        precio_venta INTEGER NOT NULL CHECK (precio_venta >= 0),
        stock_actual INTEGER NOT NULL DEFAULT 0,
        stock_minimo INTEGER NOT NULL CHECK (stock_minimo >= 0),
        activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0,1))
    );
    """)

    # ----------------------
    # TABLA CLIENTES
    # ----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );
    """)

    # ----------------------
    # TABLA MOVIMIENTOS
    # ----------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        cliente_id INTEGER,
        tipo_movimiento TEXT NOT NULL,
        cantidad INTEGER NOT NULL CHECK (cantidad != 0),
        fecha TEXT NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos(id),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );
    """)

    conn.commit()
    conn.close()


# ======================================================
# PRODUCTOS
# ======================================================

def insertar_producto(codigo, nombre, precio_venta, stock_inicial, stock_minimo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO productos (codigo, nombre, precio_venta, stock_actual, stock_minimo)
    VALUES (?, ?, ?, ?, ?)
    """, (codigo, nombre, precio_venta, stock_inicial, stock_minimo))

    conn.commit()
    conn.close()


def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, codigo, nombre, precio_venta, stock_actual, stock_minimo, activo
    FROM productos
    WHERE activo = 1
    ORDER BY nombre ASC
    """)

    productos = cursor.fetchall()
    conn.close()
    return productos


# ======================================================
# STOCK
# ======================================================

def obtener_stock_producto(producto_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stock_actual
    FROM productos
    WHERE id = ?
    """, (producto_id,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return None

    return resultado[0]


def obtener_stock_y_minimo(producto_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stock_actual, stock_minimo
    FROM productos
    WHERE id = ?
    """, (producto_id,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return None

    return resultado  # (stock_actual, stock_minimo)


# ======================================================
# CLIENTES
# ======================================================

def obtener_o_crear_cliente(nombre_cliente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM clientes WHERE nombre = ?",
        (nombre_cliente,)
    )
    resultado = cursor.fetchone()

    if resultado:
        conn.close()
        return resultado[0]

    cursor.execute(
        "INSERT INTO clientes (nombre) VALUES (?)",
        (nombre_cliente,)
    )
    conn.commit()

    cliente_id = cursor.lastrowid
    conn.close()
    return cliente_id


def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nombre
    FROM clientes
    ORDER BY nombre ASC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos


# ======================================================
# MOVIMIENTOS
# ======================================================

def registrar_movimiento(producto_id, tipo_movimiento, cantidad, cliente_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO movimientos_inventario
        (producto_id, cliente_id, tipo_movimiento, cantidad, fecha)
        VALUES (?, ?, ?, ?, ?)
        """, (producto_id, cliente_id, tipo_movimiento, cantidad, fecha))

        cursor.execute("""
        UPDATE productos
        SET stock_actual = stock_actual + ?
        WHERE id = ?
        """, (cantidad, producto_id))

        conn.commit()
        return True, "Movimiento registrado correctamente."

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


def obtener_salidas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        p.codigo,
        p.nombre,
        m.fecha,
        m.cantidad,
        c.nombre
    FROM movimientos_inventario m
    JOIN productos p ON p.id = m.producto_id
    LEFT JOIN clientes c ON c.id = m.cliente_id
    WHERE m.tipo_movimiento = 'SALIDA'
    ORDER BY m.fecha DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

# ======================================================
# MOVIMIENTOS POR PRODUCTO
# ======================================================

def obtener_movimientos_producto(producto_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        m.id,
        m.tipo_movimiento,
        m.cantidad,
        m.fecha,
        c.nombre
    FROM movimientos_inventario m
    LEFT JOIN clientes c ON c.id = m.cliente_id
    WHERE m.producto_id = ?
    ORDER BY m.fecha ASC
    """, (producto_id,))

    datos = cursor.fetchall()
    conn.close()
    return datos