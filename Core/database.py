import sqlite3
from datetime import datetime

DB_NAME = "inventario.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # Activar claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_venta INTEGER NOT NULL CHECK (precio_venta >= 0),
        stock_actual INTEGER NOT NULL,
        stock_minimo INTEGER NOT NULL CHECK (stock_minimo >= 0),
        activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0,1))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        tipo_movimiento TEXT NOT NULL,
        cantidad INTEGER NOT NULL CHECK (cantidad != 0),
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

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    SELECT id, nombre, precio_venta, stock_actual, stock_minimo, activo
    FROM productos
    WHERE activo = 1
    ORDER BY nombre ASC
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

def obtener_movimientos_producto(producto_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    SELECT id, tipo_movimiento, cantidad, fecha, motivo
    FROM movimientos_inventario
    WHERE producto_id = ?
    ORDER BY fecha ASC
    """, (producto_id,))

    movimientos = cursor.fetchall()
    conn.close()
    return movimientos

def obtener_salidas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        p.id,
        p.nombre,
        m.fecha,
        m.cantidad,
        m.motivo
    FROM movimientos_inventario m
    JOIN productos p ON m.producto_id = p.id
    WHERE m.tipo_movimiento = 'SALIDA'
    ORDER BY m.fecha ASC
    """)

    salidas = cursor.fetchall()
    conn.close()
    return salidas


def registrar_movimiento(producto_id, tipo_movimiento, cantidad, motivo=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON;")

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
        return True, "Movimiento persistido en base de datos"

    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, f"Error de integridad: {str(e)}"

    except Exception as e:
        conn.rollback()
        return False, f"Error inesperado: {str(e)}"

    finally:
        conn.close()