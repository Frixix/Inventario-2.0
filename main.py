from database import (
    crear_tablas,
    insertar_producto,
    obtener_productos,
    registrar_movimiento
)

crear_tablas()

# Insertar producto inicial
insertar_producto(
    nombre="Cuaderno cuadriculado",
    precio_venta=3500,
    stock_inicial=20,
    stock_minimo=5
)

print("Producto creado\n")

# Ver productos
productos = obtener_productos()
print("Estado inicial:")
for p in productos:
    print(p)

# Registrar salida
registrar_movimiento(
    producto_id=1,
    tipo_movimiento="SALIDA",
    cantidad=3,
    motivo="Venta mostrador"
)

print("\nDespués de salida:")

productos = obtener_productos()
for p in productos:
    print(p)

# Registrar entrada
registrar_movimiento(
    producto_id=1,
    tipo_movimiento="ENTRADA",
    cantidad=10,
    motivo="Reposición proveedor"
)

print("\nDespués de entrada:")

productos = obtener_productos()
for p in productos:
    print(p)


from database import (
    crear_tablas,
    insertar_producto,
    obtener_stock_producto
)

crear_tablas()

insertar_producto("Teclado", 50000, 10, 2)

stock = obtener_stock_producto(1)
print("Stock actual:", stock)
