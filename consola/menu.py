from abc import ABC, abstractmethod

from entidades.usuario import Usuario


class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self._usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú hasta que el usuario elige salir. True = cerrar sesión, False = salir."""
        ...
