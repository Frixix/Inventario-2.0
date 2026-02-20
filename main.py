from database import (
    crear_tablas,
    insertar_producto,
    obtener_productos
)

from logica_inventario import (
    salida_producto,
    entrada_producto,
    ajuste_admin,
    verificar_stock_minimo
)


def main():
    crear_tablas()

    insertar_producto(
        nombre="Cuaderno cuadriculado",
        precio_venta=3500,
        stock_inicial=20,
        stock_minimo=5
    )

    print("Inventario inicial:")
    for producto in obtener_productos():
        print(producto)

    print("\nSalida de inventario:")
    ok, mensaje = salida_producto(1, 5)
    print(mensaje)

    print("\nEntrada de inventario:")
    ok, mensaje = entrada_producto(1, 3)
    print(mensaje)

    print("\nAjuste administrativo:")
    ok, mensaje = ajuste_admin(1, -3, "Producto dañado")
    print(mensaje)

    print("\nInventario final:")
    for producto in obtener_productos():
        print(producto)

    alerta, mensaje = verificar_stock_minimo(1)
    print("\nEstado de stock:")
    print(mensaje)


if __name__ == "__main__":
    main()