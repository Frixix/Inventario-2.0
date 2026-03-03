from core.database import (
    obtener_stock_producto,
    obtener_stock_y_minimo,
    registrar_movimiento,
    obtener_movimientos_producto,
    insertar_producto
)


def _aplicar_movimiento(producto_id, tipo_movimiento, cantidad, motivo):
    """
    Aplica cualquier movimiento de inventario
    garantizando que el stock no quede negativo.
    """

    stock_actual = obtener_stock_producto(producto_id)

    if stock_actual is None:
        return False, "El producto no existe"

    stock_resultante = stock_actual + cantidad

    if stock_resultante < 0:
        return False, (
            f"Operación inválida. Stock insuficiente "
            f"(actual: {stock_actual})"
        )

    ok, mensaje = registrar_movimiento(
        producto_id=producto_id,
        tipo_movimiento=tipo_movimiento,
        cantidad=cantidad,
        motivo=motivo
    )

    if not ok:
        return False, mensaje

    return True, "Movimiento registrado correctamente"


def salida_producto(producto_id, cantidad, motivo="Salida de inventario"):
    if cantidad <= 0:
        return False, "La cantidad debe ser mayor que cero"

    return _aplicar_movimiento(
        producto_id=producto_id,
        tipo_movimiento="SALIDA",
        cantidad=-cantidad,
        motivo=motivo
    )


def entrada_producto(producto_id, cantidad, motivo="Entrada de inventario"):
    if cantidad <= 0:
        return False, "La cantidad de entrada debe ser mayor que cero"

    return _aplicar_movimiento(
        producto_id=producto_id,
        tipo_movimiento="ENTRADA",
        cantidad=cantidad,
        motivo=motivo
    )


def ajuste_admin(producto_id, cantidad, motivo):
    if not motivo or motivo.strip() == "":
        return False, "El motivo del ajuste es obligatorio"

    return _aplicar_movimiento(
        producto_id=producto_id,
        tipo_movimiento="AJUSTE_ADMIN",
        cantidad=cantidad,
        motivo=motivo
    )


def verificar_stock_minimo(producto_id):
    datos = obtener_stock_y_minimo(producto_id)

    if datos is None:
        return False, "El producto no existe"

    stock_actual, stock_minimo = datos

    if stock_actual <= stock_minimo:
        return True, (
            f"ALERTA: Stock bajo "
            f"(actual: {stock_actual}, mínimo: {stock_minimo})"
        )

    return False, "Stock en nivel normal"

def ver_historial_producto(producto_id):
    movimientos = obtener_movimientos_producto(producto_id)

    if not movimientos:
        return False, "No hay movimientos registrados"

    return True, movimientos

from core.database import obtener_productos


def listar_productos():
    return obtener_productos()

def crear_producto(nombre, precio, stock, minimo):

    if not nombre or nombre.strip() == "":
        return False, "El nombre es obligatorio"

    if precio <= 0:
        return False, "El precio debe ser mayor que cero"

    if stock < 0:
        return False, "El stock no puede ser negativo"

    if minimo < 0:
        return False, "El stock mínimo no puede ser negativo"

    insertar_producto(nombre, precio, stock, minimo)

    return True, "Producto creado correctamente"