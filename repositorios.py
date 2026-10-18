from abc import ABC, abstractmethod
import json
from pathlib import Path


class RepositorioInventario(ABC):
    """Contrato de persistencia; la lógica no depende de un archivo concreto."""

    @abstractmethod
    def guardar_productos(self, productos):
        raise NotImplementedError

    @abstractmethod
    def cargar_productos(self):
        raise NotImplementedError


class RepositorioJSON(RepositorioInventario):
    def __init__(self, ruta="inventario.json"):
        self.ruta = Path(ruta)

    def guardar_productos(self, productos):
        datos = [
            {
                "codigo": p.codigo,
                "nombre": p.nombre,
                "precio": p.precio,
                "cantidad": p.cantidad,
                "tipo": p.__class__.__name__
            }
            for p in productos
        ]
        temporal = self.ruta.with_suffix(".tmp")
        temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        temporal.replace(self.ruta)

    def cargar_productos(self):
        if not self.ruta.exists():
            return []

        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
            if not isinstance(datos, list):
                raise ValueError("El inventario debe contener una lista de productos.")

            # Los tipos concretos se registran automáticamente al definirse
            # como subclases de Producto. No hay que editar este repositorio
            # para incorporar una nueva clase de producto.
            from productos import Producto
            tipos = Producto.tipos_registrados()

            productos = []
            codigos = set()
            for registro in datos:
                codigo = registro["codigo"]
                if codigo in codigos:
                    raise ValueError(f"Código duplicado en inventario: {codigo}")
                codigos.add(codigo)

                tipo = registro["tipo"]
                if tipo not in tipos:
                    raise ValueError(f"Tipo de producto desconocido: {tipo}")

                productos.append(tipos[tipo](
                    registro["codigo"],
                    registro["nombre"],
                    float(registro["precio"]),
                    int(registro["cantidad"])
                ))
            return productos
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            raise ValueError(f"El archivo de inventario está corrupto: {error}") from error


class RepositorioEnMemoria(RepositorioInventario):
    """Repositorio sencillo para pruebas automatizadas."""
    def __init__(self):
        self._productos = []

    def guardar_productos(self, productos):
        self._productos = list(productos)

    def cargar_productos(self):
        return list(self._productos)
