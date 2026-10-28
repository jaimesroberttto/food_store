from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from entidades.usuario import Usuario
from enums.rol import Rol
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def crear_menu(
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
) -> Menu:
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(
            usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio
        )
    return MenuCliente(usuario, categoria_servicio, producto_servicio, pedido_servicio)
