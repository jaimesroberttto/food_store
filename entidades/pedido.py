from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.errores import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    StockInsuficienteError,
)

_TRANSICIONES_VALIDAS: dict[Estado, set[Estado]] = {
    Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
    Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
    Estado.TERMINADO: set(),
    Estado.CANCELADO: set(),
}


class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario is None or usuario.eliminado:
            raise DatoInvalidoError("El pedido necesita un usuario válido")
        self.__usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.forma_pago = forma_pago
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago no es válida")
        self.__forma_pago = valor

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if producto is None or producto.eliminado:
            raise DatoInvalidoError("El producto no es válido")
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0")
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}' (disponible: {producto.stock})"
            )

        detalle_existente = self.buscar_detalle_por_producto(producto)
        if detalle_existente is not None:
            detalle_existente.aumentar_cantidad(cantidad)
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))

        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise DatoInvalidoError("El pedido no tiene un detalle con ese producto")
        self.__detalles.remove(detalle)
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        if not isinstance(nuevo_estado, Estado):
            raise DatoInvalidoError("El estado no es válido")
        if nuevo_estado not in _TRANSICIONES_VALIDAS[self.__estado]:
            raise OperacionNoPermitidaError(
                f"No se puede pasar de {self.__estado.value} a {nuevo_estado.value}"
            )
        self.__estado = nuevo_estado

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.usuario.nombre} {self.usuario.apellido} - "
            f"{self.estado.value} - {self.forma_pago.value} - ${self.total:.2f} - {self.fecha}"
        )
