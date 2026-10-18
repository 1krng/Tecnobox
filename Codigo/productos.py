from abc import ABC, abstractmethod


class Producto(ABC):
    """Abstracción común de los productos que puede vender Tecnobox."""

    _tipos_registrados = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "__abstractmethods__", None):
            Producto._tipos_registrados[cls.__name__] = cls

    @classmethod
    def tipos_registrados(cls):
        return dict(cls._tipos_registrados)

    def __init__(self, codigo: str, nombre: str, precio: float, cantidad: int):
        if not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        self._codigo = codigo
        self._nombre = nombre
        self._precio = float(precio)
        self._cantidad = int(cantidad)

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def cantidad(self):
        return self._cantidad

    def retirar_stock(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser mayor que cero.")
        if cantidad > self._cantidad:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self._cantidad -= cantidad

    def reponer_stock(self, cantidad: int):
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que cero.")
        self._cantidad += cantidad

    @abstractmethod
    def calcular_descuento(self) -> float:
        """Devuelve el porcentaje de descuento entre 0 y 1."""
        raise NotImplementedError

    def calcular_total(self, cantidad: int) -> float:
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self._cantidad:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        return self._precio * cantidad * (1 - self.calcular_descuento())


class ProductoNormal(Producto):
    def calcular_descuento(self) -> float:
        return 0.0


class ProductoPerecible(Producto):
    def calcular_descuento(self) -> float:
        return 0.20


class LicenciaDigital(Producto):
    def calcular_descuento(self) -> float:
        return 0.10
