"""Pantalla de administrador: gestiona categorías, productos, usuarios y pedidos."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from entidades.usuario import Usuario
from gui.pantalla import Pantalla
from gui.secciones.categorias import SeccionCategorias
from gui.secciones.pedidos import SeccionPedidos
from gui.secciones.productos import SeccionProductos
from gui.secciones.usuarios import SeccionUsuarios
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class PantallaAdministrador(Pantalla):
    def __init__(
        self,
        parent: tk.Widget,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
        on_cerrar_sesion: Callable[[], None],
        on_salir: Callable[[], None],
    ) -> None:
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__usuario_servicio = usuario_servicio
        self.__pedido_servicio = pedido_servicio
        super().__init__(parent, usuario, on_cerrar_sesion, on_salir)

    def _titulo(self) -> str:
        return f"Administrador - {self._usuario.nombre} {self._usuario.apellido}"

    def _construir_navegacion(self, contenedor: ttk.Frame) -> None:
        ttk.Button(
            contenedor,
            text="Categorías",
            command=lambda: self._mostrar_seccion(
                lambda parent: SeccionCategorias(
                    parent, self.__categoria_servicio, self.__producto_servicio
                )
            ),
        ).pack(fill="x", pady=4)
        ttk.Button(
            contenedor,
            text="Productos",
            command=lambda: self._mostrar_seccion(
                lambda parent: SeccionProductos(
                    parent, self.__producto_servicio, self.__categoria_servicio
                )
            ),
        ).pack(fill="x", pady=4)
        ttk.Button(
            contenedor,
            text="Usuarios",
            command=lambda: self._mostrar_seccion(
                lambda parent: SeccionUsuarios(parent, self.__usuario_servicio, self._usuario)
            ),
        ).pack(fill="x", pady=4)
        ttk.Button(
            contenedor,
            text="Pedidos",
            command=lambda: self._mostrar_seccion(
                lambda parent: SeccionPedidos(
                    parent, self.__pedido_servicio, self.__usuario_servicio, self.__producto_servicio
                )
            ),
        ).pack(fill="x", pady=4)
