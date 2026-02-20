from database import (
    obtener_stock_producto,
    registrar_movimiento
)


def salida_producto(producto_id, cantidad, motivo="Salida de inventario"):
    """
    Registra una salida de inventario validando reglas de negocio.
    """

    # Validaciones básicas
    if cantidad <= 0:
        return False, "La cantidad debe ser mayor que cero"

    stock_actual = obtener_stock_producto(producto_id)

    if stock_actual is None:
        return False, "El producto no existe"

    if stock_actual < cantidad:
        return False, f"Stock insuficiente. Disponible: {stock_actual}"

    # Si pasa todas las validaciones, se registra el movimiento
    registrar_movimiento(
        producto_id=producto_id,
        tipo_movimiento="SALIDA",
        cantidad=cantidad,
        motivo=motivo
    )

    return True, "Salida registrada correctamente"
