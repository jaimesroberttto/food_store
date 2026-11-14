"""Ventana raíz de Food Store: orquesta login, pantalla principal y cierre de sesión."""

import tkinter as tk
from tkinter import ttk

from entidades.usuario import Usuario
from gui.pantalla import crear_pantalla
from gui.pantalla_login import PantallaLogin
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class FoodStoreApp(tk.Tk):
    def __init__(
        self,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        super().__init__()
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__usuario_servicio = usuario_servicio
        self.__pedido_servicio = pedido_servicio
        self.__frame_actual: tk.Widget | None = None

        self.title("Food Store")
        self.geometry("960x600")
        self.minsize(800, 500)

        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        self.mostrar_login()

    def mostrar_login(self) -> None:
        login = PantallaLogin(
            self, self.__usuario_servicio, self.__on_login_exitoso, self.__on_intentos_agotados
        )
        self.__cambiar_frame(login)

    def __cambiar_frame(self, frame: tk.Widget) -> None:
        if self.__frame_actual is not None:
            self.__frame_actual.destroy()
        self.__frame_actual = frame
        frame.pack(fill="both", expand=True)

    def __on_login_exitoso(self, usuario: Usuario) -> None:
        pantalla = crear_pantalla(
            self,
            usuario,
            self.__categoria_servicio,
            self.__producto_servicio,
            self.__usuario_servicio,
            self.__pedido_servicio,
            self.mostrar_login,
            self.destroy,
        )
        self.__cambiar_frame(pantalla)

    def __on_intentos_agotados(self) -> None:
        self.destroy()
