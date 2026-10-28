from entidades.base import Base
from entidades.producto import Producto
from excepciones.errores import DatoInvalidoError


class DetallePedido(Base):
    """Nace y muere con su pedido: solo Pedido crea instancias de esta clase."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__producto = producto
        self.__subtotal: float = 0.0
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if valor <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0")
        self.__cantidad = int(valor)
        self.__subtotal = self.__cantidad * self.__producto.precio

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def aumentar_cantidad(self, cantidad_adicional: int) -> None:
        if cantidad_adicional <= 0:
            raise DatoInvalidoError("La cantidad a agregar debe ser mayor a 0")
        self.cantidad = self.cantidad + cantidad_adicional

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal:.2f}"
