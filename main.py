from gestor_inventario import GestorInventario
from productos import ProductoNormal, ProductoPerecible, LicenciaDigital
from repositorios import RepositorioJSON
from salidas import SalidaConsola


def mostrar_inventario(gestor):
    print("\n========== INVENTARIO TECNOBOX ==========")
    for producto in gestor.listar_productos():
        print(
            f"{producto.codigo} | {producto.nombre} | "
            f"Tipo: {producto.__class__.__name__} | "
            f"Precio: ${producto.precio:.2f} | Stock: {producto.cantidad}"
        )


def cargar_datos_iniciales(gestor):
    if gestor.listar_productos():
        return

    gestor.agregar_producto(ProductoNormal("TEC-001", "Teclado USB", 12990, 10))
    gestor.agregar_producto(ProductoPerecible("TEC-002", "Pasta térmica", 5990, 8))
    gestor.agregar_producto(LicenciaDigital("TEC-003", "Licencia antivirus", 19990, 20))


def main():
    gestor = GestorInventario(RepositorioJSON(), SalidaConsola())
    cargar_datos_iniciales(gestor)
    mostrar_inventario(gestor)

    print("\n========== VENTA DE DEMOSTRACIÓN ==========")
    try:
        total = gestor.vender("TEC-002", 2)
        print(f"Venta procesada. Total pagado: ${total:.2f}")
    except ValueError as error:
        print(f"No se pudo completar la operación: {error}")

    mostrar_inventario(gestor)
    print("\nLos datos quedan guardados en inventario.json.")


if __name__ == "__main__":
    main()
