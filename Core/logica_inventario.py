from core.database import (
    insertar_producto,
    obtener_productos,
    registrar_movimiento,
    obtener_stock_producto,
    obtener_stock_y_minimo,
    obtener_o_crear_cliente
)


# ======================================================
# PRODUCTOS
# ======================================================

def crear_producto(codigo, nombre, precio, stock, minimo):

    if not codigo.strip():
        return False, "El código es obligatorio."

    if not nombre.strip():
        return False, "El nombre es obligatorio."

    if precio < 0:
        return False, "El precio no puede ser negativo."

    if stock < 0:
        return False, "El stock inicial no puede ser negativo."

    if minimo < 0:
        return False, "El stock mínimo no puede ser negativo."

    try:
        insertar_producto(codigo, nombre, precio, stock, minimo)
        return True, "Producto creado correctamente."
    except Exception as e:
        return False, str(e)


def listar_productos():
    return obtener_productos()


# ======================================================
# ENTRADAS
# ======================================================

def entrada_producto(producto_id, cantidad):

    if cantidad <= 0:
        return False, "La cantidad debe ser mayor a cero."

    return registrar_movimiento(
        producto_id,
        "ENTRADA",
        cantidad,
        None
    )


# ======================================================
# SALIDAS
# ======================================================

def salida_producto(producto_id, cantidad, nombre_cliente):

    if cantidad <= 0:
        return False, "La cantidad debe ser mayor a cero."

    stock_actual = obtener_stock_producto(producto_id)

    if stock_actual is None:
        return False, "Producto no encontrado."

    if cantidad > stock_actual:
        return False, "No hay stock suficiente."

    cliente_id = obtener_o_crear_cliente(nombre_cliente)

    return registrar_movimiento(
        producto_id,
        "SALIDA",
        -cantidad,
        cliente_id
    )