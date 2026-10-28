from entidades.base import Base
from excepciones.errores import DatoInvalidoError


class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre de la categoría no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("La descripción de la categoría no puede estar vacía")
        self.__descripcion = valor.strip()

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - {self.descripcion}"
