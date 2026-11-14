"""Clase abstracta Pantalla: resuelve la vista principal por polimorfismo según el rol."""

from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from typing import Callable

from entidades.usuario import Usuario
from enums.rol import Rol
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class Pantalla(ttk.Frame, ABC):
    def __init__(
        self,
        parent: tk.Widget,
        usuario: Usuario,
        on_cerrar_sesion: Callable[[], None],
        on_salir: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self._usuario = usuario
        self.__on_cerrar_sesion = on_cerrar_sesion
        self.__on_salir = on_salir
        self.__contenido: tk.Widget | None = None
        self.__area_contenido: ttk.Frame
        self.__construir_layout()

    def __construir_layout(self) -> None:
        encabezado = ttk.Frame(self, padding=10)
        encabezado.pack(fill="x")
        ttk.Label(encabezado, text=self._titulo(), font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Button(encabezado, text="Salir", command=self.__on_salir).pack(side="right")
        ttk.Button(encabezado, text="Cerrar sesión", command=self.__on_cerrar_sesion).pack(
            side="right", padx=6
        )

        ttk.Separator(self).pack(fill="x")

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True)

        barra_navegacion = ttk.Frame(cuerpo, padding=10, width=200)
        barra_navegacion.pack(side="left", fill="y")
        barra_navegacion.pack_propagate(False)

        self.__area_contenido = ttk.Frame(cuerpo, padding=10)
        self.__area_contenido.pack(side="left", fill="both", expand=True)

        self._construir_navegacion(barra_navegacion)

    @abstractmethod
    def _titulo(self) -> str:
        ...

    @abstractmethod
    def _construir_navegacion(self, contenedor: ttk.Frame) -> None:
        ...

    def _mostrar_seccion(self, construir_seccion: Callable[[tk.Widget], tk.Widget]) -> None:
        if self.__contenido is not None:
            self.__contenido.destroy()
        self.__contenido = construir_seccion(self.__area_contenido)
        self.__contenido.pack(fill="both", expand=True)


def crear_pantalla(
    parent: tk.Widget,
    usuario: Usuario,
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
    pedido_servicio: PedidoServicio,
    on_cerrar_sesion: Callable[[], None],
    on_salir: Callable[[], None],
) -> Pantalla:
    from gui.pantalla_administrador import PantallaAdministrador
    from gui.pantalla_cliente import PantallaCliente

    if usuario.rol == Rol.ADMIN:
        return PantallaAdministrador(
            parent,
            usuario,
            categoria_servicio,
            producto_servicio,
            usuario_servicio,
            pedido_servicio,
            on_cerrar_sesion,
            on_salir,
        )
    return PantallaCliente(
        parent,
        usuario,
        categoria_servicio,
        producto_servicio,
        pedido_servicio,
        on_cerrar_sesion,
        on_salir,
    )
