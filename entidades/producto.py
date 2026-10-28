from entidades.base import Base
from entidades.categoria import Categoria
from excepciones.errores import DatoInvalidoError, PrecioInvalidoError


class Producto(Base):
    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise PrecioInvalidoError("El precio no puede ser negativo")
        self.__precio = float(valor)

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = valor.strip() if valor else ""

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        if valor < 0:
            raise DatoInvalidoError("El stock no puede ser negativo")
        self.__stock = int(valor)

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = valor.strip() if valor else ""

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = bool(valor)

    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if valor is None or valor.eliminado:
            raise DatoInvalidoError("La categoría del producto no es válida")
        self.__categoria = valor

    def __str__(self) -> str:
        disponibilidad = "disponible" if self.disponible else "no disponible"
        return (
            f"[{self.id}] {self.nombre} - ${self.precio:.2f} - stock: {self.stock} "
            f"- {self.categoria.nombre} ({disponibilidad})"
        )
