from entidades.pedido import Pedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.errores import EntidadNoEncontradaError
from servicios.producto_servicio import ProductoServicio


class PedidoServicio:
    def __init__(self, producto_servicio: ProductoServicio) -> None:
        self.__pedidos: list[Pedido] = []
        self.__producto_servicio = producto_servicio

    def listar(self) -> list[Pedido]:
        return [pedido for pedido in self.__pedidos if not pedido.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [pedido for pedido in self.listar() if pedido.usuario == usuario]

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for pedido in self.__pedidos:
            if pedido.id == id_pedido and not pedido.eliminado:
                return pedido
        raise EntidadNoEncontradaError(f"No existe el pedido con id {id_pedido}")

    def crear(
        self, usuario: Usuario, forma_pago: FormaPago, items: list[tuple[int, Producto]]
    ) -> Pedido:
        pedido = Pedido(usuario, forma_pago)
        for cantidad, producto in items:
            pedido.agregar_detalle(cantidad, producto)
        for detalle in pedido.detalles:
            self.__producto_servicio.descontar_stock(detalle.producto, detalle.cantidad)
        self.__pedidos.append(pedido)
        return pedido

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        estado_anterior = pedido.estado
        pedido.cambiar_estado(nuevo_estado)
        if nuevo_estado == Estado.CANCELADO and estado_anterior != Estado.CANCELADO:
            self._devolver_stock(pedido)
        return pedido

    def cambiar_forma_pago(self, id_pedido: int, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, id_pedido: int) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self._devolver_stock(pedido)
        pedido.eliminado = True
        return pedido

    def _devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            self.__producto_servicio.devolver_stock(detalle.producto, detalle.cantidad)
