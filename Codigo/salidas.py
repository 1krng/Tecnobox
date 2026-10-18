from abc import ABC, abstractmethod


class SalidaTicket(ABC):
    @abstractmethod
    def mostrar(self, mensaje: str):
        raise NotImplementedError


class SalidaConsola(SalidaTicket):
    def mostrar(self, mensaje: str):
        print(mensaje)


class SalidaMemoria(SalidaTicket):
    """Salida utilizada en pruebas, para comprobar el ticket sin imprimirlo."""
    def __init__(self):
        self.mensajes = []

    def mostrar(self, mensaje: str):
        self.mensajes.append(mensaje)
