from database import (
    crear_tablas,
    insertar_producto,
    obtener_productos,
    obtener_stock_producto,
    registrar_movimiento
)

# Inicialización
crear_tablas()

# Crear producto de prueba (solo una vez)
insertar_producto(
    nombre="Cuaderno cuadriculado",
    precio_venta=3500,
    stock_inicial=20,
    stock_minimo=5
)

# Mostrar productos
print("Estado inicial del inventario:")
productos = obtener_productos()
for p in productos:
    print(p)

# Intentar salida
producto_id = 1
cantidad_salida = 15

stock_actual = obtener_stock_producto(producto_id)

print("\nIntentando salida...")

if stock_actual is None:
    print("Error: producto no encontrado")

elif cantidad_salida <= 0:
    print("Error: cantidad inválida")

elif stock_actual < cantidad_salida:
    print("Error: stock insuficiente")
    print(f"Stock disponible: {stock_actual}")

else:
    registrar_movimiento(
        producto_id=producto_id,
        tipo_movimiento="SALIDA",
        cantidad=cantidad_salida,
        motivo="Venta mostrador"
    )
    print("Salida registrada correctamente")

# Estado final
print("\nEstado final del inventario:")
productos = obtener_productos()
for p in productos:
    print(p)