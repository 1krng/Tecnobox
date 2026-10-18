"""
VERSIÓN ANTES: ejemplo intencionalmente defectuoso.
Esta clase viola SRP porque calcula el stock, calcula descuentos,
muestra el ticket y guarda información desde el mismo módulo.
También viola OCP porque cada nuevo tipo de producto exige modificar
los condicionales de calcular_descuento().
No se recomienda usar esta versión en producción.
"""

class GestorInventario:
    def __init__(self, archivo="inventario_defectuoso.txt"):
        self.archivo = archivo
        self.productos = []

    def agregar_producto(self, nombre, tipo, precio, cantidad):
        self.productos.append({
            "nombre": nombre,
            "tipo": tipo,
            "precio": precio,
            "cantidad": cantidad
        })

    def calcular_total(self, producto):
        if producto["tipo"] == "normal":
            descuento = 0
        elif producto["tipo"] == "perecible":
            descuento = 0.20
        elif producto["tipo"] == "licencia":
            descuento = 0.10
        else:
            descuento = 0

        return producto["precio"] * producto["cantidad"] * (1 - descuento)

    def procesar_venta(self, indice):
        producto = self.productos[indice]
        total = self.calcular_total(producto)

        # Responsabilidad de presentación mezclada con lógica de negocio.
        ticket = (
            f"--- TICKET ---\n"
            f"Producto: {producto['nombre']}\n"
            f"Cantidad: {producto['cantidad']}\n"
            f"Total: ${total:.2f}\n"
        )
        print(ticket)

        # Responsabilidad de persistencia mezclada con la venta.
        with open(self.archivo, "a", encoding="utf-8") as archivo:
            archivo.write(ticket)

        return total
