from Core.database import (
    crear_tablas,
    insertar_producto,
    obtener_productos
)

from Core.logica_inventario import (
    salida_producto,
    entrada_producto,
    ajuste_admin,
    ver_historial_producto
)


# ==============================
# FUNCIONES DE VALIDACIÓN
# ==============================

def pedir_entero(mensaje, permitir_negativo=False, permitir_cero=False):
    while True:
        try:
            valor = int(input(mensaje))

            if not permitir_negativo and valor < 0:
                print("No se permiten números negativos.")
                continue

            if not permitir_cero and valor == 0:
                print("El valor debe ser diferente de 0.")
                continue

            return valor

        except ValueError:
            print("Debe ingresar un número entero válido.")


# ==============================
# FUNCIONES DE PRESENTACIÓN
# ==============================

def mostrar_productos():
    productos = obtener_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    print("\n=== LISTA DE PRODUCTOS ===")

    for p in productos:
        id_, nombre, precio, stock, minimo, activo = p
        alerta = "⚠ STOCK BAJO" if stock <= minimo else ""

        print(
            f"ID: {id_} | "
            f"Producto: {nombre} | "
            f"Precio: ${precio} | "
            f"Stock: {stock} | "
            f"Mínimo: {minimo} {alerta}"
        )


def menu():
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("1. Registrar producto")
    print("2. Entrada de inventario")
    print("3. Salida de inventario")
    print("4. Ajuste administrativo")
    print("5. Ver productos")
    print("6. Ver historial de producto")
    print("7. Salir")


# ==============================
# PROGRAMA PRINCIPAL
# ==============================

def main():
    crear_tablas()

    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            precio = pedir_entero("Precio de venta: ", permitir_negativo=False, permitir_cero=False)
            stock = pedir_entero("Stock inicial: ", permitir_negativo=False, permitir_cero=True)
            minimo = pedir_entero("Stock mínimo: ", permitir_negativo=False, permitir_cero=True)

            insertar_producto(nombre, precio, stock, minimo)
            print("Producto registrado.")

        elif opcion == "2":
            mostrar_productos()
            producto_id = pedir_entero("ID del producto: ")
            cantidad = pedir_entero("Cantidad de entrada: ", permitir_negativo=False, permitir_cero=False)

            ok, mensaje = entrada_producto(producto_id, cantidad)
            print(mensaje)

        elif opcion == "3":
            mostrar_productos()
            producto_id = pedir_entero("ID del producto: ")
            cantidad = pedir_entero("Cantidad de salida: ", permitir_negativo=False, permitir_cero=False)

            ok, mensaje = salida_producto(producto_id, cantidad)
            print(mensaje)

        elif opcion == "4":
            mostrar_productos()
            producto_id = pedir_entero("ID del producto: ")
            cantidad = pedir_entero("Cantidad (negativo para reducir): ", permitir_negativo=True, permitir_cero=False)
            motivo = input("Motivo del ajuste: ").strip()

            ok, mensaje = ajuste_admin(producto_id, cantidad, motivo)
            print(mensaje)

        elif opcion == "5":
            mostrar_productos()

        elif opcion == "6":
            mostrar_productos()
            producto_id = pedir_entero("ID del producto: ")

            ok, datos = ver_historial_producto(producto_id)

            if ok:
                print("\n=== HISTORIAL ===")
                for movimiento in datos:
                    print(movimiento)
            else:
                print(datos)

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()