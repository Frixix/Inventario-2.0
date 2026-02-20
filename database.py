import sqlite3
from datetime import datetime

DB_NAME = "inventario.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_venta INTEGER NOT NULL,
        stock_actual INTEGER NOT NULL,
        stock_minimo INTEGER NOT NULL,
        activo INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        tipo_movimiento TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        motivo TEXT,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    );
    """)

    conn.commit()
    conn.close()


def insertar_producto(nombre, precio_venta, stock_inicial, stock_minimo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO productos (nombre, precio_venta, stock_actual, stock_minimo)
    VALUES (?, ?, ?, ?)
    """, (nombre, precio_venta, stock_inicial, stock_minimo))

    conn.commit()
    conn.close()


def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nombre, stock_actual
    FROM productos
    """)

    productos = cursor.fetchall()
    conn.close()
    return productos


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


def registrar_movimiento(producto_id, tipo_movimiento, cantidad, motivo=None):
    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO movimientos_inventario
    (producto_id, tipo_movimiento, cantidad, fecha, motivo)
    VALUES (?, ?, ?, ?, ?)
    """, (producto_id, tipo_movimiento, cantidad, fecha, motivo))

    cursor.execute("""
    UPDATE productos
    SET stock_actual = stock_actual + ?
    WHERE id = ?
    """, (cantidad, producto_id))

    conn.commit()
    conn.close()