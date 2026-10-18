from productos import Producto
from repositorios import RepositorioInventario
from salidas import SalidaTicket


class GestorInventario:
    """
    Coordina las operaciones de inventario.
    Recibe sus dependencias por constructor (DIP): no crea directamente
    un repositorio ni decide cómo se muestra el ticket.
    """
    def __init__(self, repositorio: RepositorioInventario, salida: SalidaTicket):
        self._repositorio = repositorio
        self._salida = salida
        self._productos = self._repositorio.cargar_productos()

    def listar_productos(self):
        return list(self._productos)

    def agregar_producto(self, producto: Producto):
        if any(p.codigo == producto.codigo for p in self._productos):
            raise ValueError(f"Ya existe un producto con código {producto.codigo}.")
        self._productos.append(producto)
        self._repositorio.guardar_productos(self._productos)

    def buscar_producto(self, codigo: str):
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def reponer_stock(self, codigo: str, cantidad: int):
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No existe el producto {codigo}.")
        producto.reponer_stock(cantidad)
        self._repositorio.guardar_productos(self._productos)

    def vender(self, codigo: str, cantidad: int) -> float:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No existe el producto {codigo}.")

        total = producto.calcular_total(cantidad)
        producto.retirar_stock(cantidad)
        self._repositorio.guardar_productos(self._productos)

        ticket = (
            "--- TICKET TECNOBOX ---\n"
            f"Producto: {producto.nombre}\n"
            f"Código: {producto.codigo}\n"
            f"Cantidad: {cantidad}\n"
            f"Total: ${total:.2f}\n"
            f"Stock restante: {producto.cantidad}"
        )
        self._salida.mostrar(ticket)
        return total
