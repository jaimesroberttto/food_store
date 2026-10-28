"""Pruebas del modelo y los servicios, sin pasar por la consola interactiva."""

from entidades.base import Base
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones.errores import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    PrecioInvalidoError,
    StockInsuficienteError,
)
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def main() -> None:
    Base._contador_id = 0  # reinicia el contador para que las pruebas sean reproducibles

    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio()
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(producto_servicio)

    titulo("Categorías - caso válido")
    bebidas = categoria_servicio.crear("Bebidas", "Gaseosas, jugos y aguas")
    comidas = categoria_servicio.crear("Comidas", "Platos principales")
    for categoria in categoria_servicio.listar():
        print(categoria)

    titulo("Categorías - nombre duplicado (error esperado)")
    try:
        categoria_servicio.crear("bebidas", "Duplicada")
    except DuplicadoError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Productos - caso válido")
    coca = producto_servicio.crear("Coca-Cola 500ml", 1500.0, "Gaseosa", 20, "", True, bebidas)
    hamburguesa = producto_servicio.crear(
        "Hamburguesa clásica", 5200.0, "Con papas", 5, "", True, comidas
    )
    for producto in producto_servicio.listar():
        print(producto)

    titulo("Productos - precio negativo (error esperado)")
    try:
        producto_servicio.crear("Producto inválido", -10.0, "x", 1, "", True, bebidas)
    except PrecioInvalidoError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Usuarios - caso válido")
    admin = usuario_servicio.crear("Ana", "Pérez", "admin@foodstore.com", "", "admin123", Rol.ADMIN)
    cliente = usuario_servicio.crear(
        "Juan", "Gómez", "cliente@foodstore.com", "", "cliente123", Rol.USUARIO
    )
    for usuario in usuario_servicio.listar():
        print(usuario)

    titulo("Usuarios - mail duplicado (error esperado)")
    try:
        usuario_servicio.crear("Otro", "Usuario", "ADMIN@foodstore.com", "", "123456", Rol.USUARIO)
    except DuplicadoError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Login - caso válido")
    autenticado = usuario_servicio.autenticar("admin@foodstore.com", "admin123")
    print(f"OK: {autenticado}")

    titulo("Login - contraseña incorrecta (error esperado)")
    try:
        usuario_servicio.autenticar("admin@foodstore.com", "incorrecta")
    except CredencialesInvalidasError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Pedidos - caso válido")
    pedido = pedido_servicio.crear(cliente, FormaPago.EFECTIVO, [(2, coca), (1, hamburguesa)])
    print(pedido)
    for detalle in pedido.detalles:
        print(f"    - {detalle}")
    print(f"Stock Coca-Cola luego del pedido: {coca.stock}")
    print(f"Stock Hamburguesa luego del pedido: {hamburguesa.stock}")

    titulo("Pedidos - stock insuficiente (error esperado)")
    try:
        pedido_servicio.crear(cliente, FormaPago.TARJETA, [(100, coca)])
    except StockInsuficienteError as error:
        print(f"OK, se rechazó: {error}")
    print(f"Stock Coca-Cola sin cambios: {coca.stock}")

    titulo("Pedidos - transición de estado inválida (error esperado)")
    try:
        pedido_servicio.cambiar_estado(pedido.id, Estado.TERMINADO)
    except OperacionNoPermitidaError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Pedidos - cancelar y devolver stock")
    pedido_servicio.cambiar_estado(pedido.id, Estado.CONFIRMADO)
    pedido_servicio.cambiar_estado(pedido.id, Estado.CANCELADO)
    print(f"Estado del pedido: {pedido.estado.value}")
    print(f"Stock Coca-Cola luego de cancelar: {coca.stock}")
    print(f"Stock Hamburguesa luego de cancelar: {hamburguesa.stock}")

    titulo("Categorías - no se puede eliminar con productos activos (error esperado)")
    try:
        activos = producto_servicio.contar_activos_por_categoria(bebidas)
        categoria_servicio.eliminar(bebidas.id, activos)
    except OperacionNoPermitidaError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Entidad no encontrada (error esperado)")
    try:
        producto_servicio.buscar_por_id(9999)
    except EntidadNoEncontradaError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Administrador no puede eliminarse a sí mismo (error esperado)")
    try:
        usuario_servicio.eliminar(admin.id, admin)
    except OperacionNoPermitidaError as error:
        print(f"OK, se rechazó: {error}")

    titulo("Fin de pruebas")


if __name__ == "__main__":
    main()
