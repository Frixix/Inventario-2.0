from database import (
    crear_tablas,
    insertar_producto,
    obtener_productos
)

from logica_inventario import salida_producto


def main():
    crear_tablas()

    # Esto es solo para pruebas iniciales
    # Luego se reemplaza por interfaz
    insertar_producto(
        nombre="Cuaderno cuadriculado",
        precio_venta=3500,
        stock_inicial=20,
        stock_minimo=5
    )

    print("Inventario inicial:")
    for producto in obtener_productos():
        print(producto)

    print("\nIntentando salida...")
    ok, mensaje = salida_producto(producto_id=1, cantidad=15)
    print(mensaje)

    print("\nInventario final:")
    for producto in obtener_productos():
        print(producto)


if __name__ == "__main__":
    main()
