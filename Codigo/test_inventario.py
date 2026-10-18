import json
import pytest

from productos import ProductoNormal, ProductoPerecible, LicenciaDigital
from gestor_inventario import GestorInventario
from repositorios import RepositorioEnMemoria, RepositorioJSON
from salidas import SalidaMemoria


def crear_gestor():
    repo = RepositorioEnMemoria()
    salida = SalidaMemoria()
    return GestorInventario(repo, salida), repo, salida


def test_venta_producto_normal_sin_descuento():
    gestor, repo, salida = crear_gestor()
    gestor.agregar_producto(ProductoNormal("A1", "Mouse", 10000, 5))

    total = gestor.vender("A1", 2)

    assert total == 20000
    assert gestor.buscar_producto("A1").cantidad == 3
    assert "Total: $20000.00" in salida.mensajes[0]


def test_producto_perecible_aplica_descuento():
    producto = ProductoPerecible("B1", "Pasta térmica", 10000, 5)
    assert producto.calcular_total(2) == 16000


def test_rechaza_venta_superior_al_stock():
    gestor, _, _ = crear_gestor()
    gestor.agregar_producto(ProductoNormal("C1", "Cable", 1000, 2))

    with pytest.raises(ValueError, match="stock suficiente"):
        gestor.vender("C1", 3)


def test_nuevo_tipo_producto_se_integra_sin_modificar_gestor():
    # Simula un nuevo tipo incorporado extendiendo la clase abstracta.
    class ProductoDePrueba(ProductoNormal):
        def calcular_descuento(self):
            return 0.05

    gestor, _, _ = crear_gestor()
    gestor.agregar_producto(ProductoDePrueba("D1", "Producto nuevo", 1000, 4))
    assert gestor.vender("D1", 1) == 950


def test_persistencia_guarda_y_recupera(tmp_path):
    ruta = tmp_path / "inventario.json"
    repo = RepositorioJSON(ruta)
    producto = ProductoNormal("E1", "Webcam", 25000, 3)
    repo.guardar_productos([producto])

    cargados = repo.cargar_productos()

    assert len(cargados) == 1
    assert cargados[0].codigo == "E1"
    assert cargados[0].cantidad == 3


def test_persistencia_controla_archivo_corrupto(tmp_path):
    ruta = tmp_path / "inventario.json"
    ruta.write_text("{dato incorrecto", encoding="utf-8")
    repo = RepositorioJSON(ruta)

    with pytest.raises(ValueError, match="corrupto"):
        repo.cargar_productos()


def test_nuevo_tipo_producto_se_persiste_sin_editar_repositorio(tmp_path):
    class ProductoEspecial(ProductoNormal):
        def calcular_descuento(self):
            return 0.15

    ruta = tmp_path / "inventario.json"
    repo = RepositorioJSON(ruta)
    producto = ProductoEspecial("F1", "Producto especial", 2000, 7)

    repo.guardar_productos([producto])
    cargados = repo.cargar_productos()

    assert len(cargados) == 1
    assert cargados[0].__class__.__name__ == "ProductoEspecial"
    assert cargados[0].calcular_total(1) == 1700
