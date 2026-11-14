"""Pantalla de cliente: solo consulta de categorías, productos, pedidos propios y datos."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from entidades.usuario import Usuario
from gui.pantalla import Pantalla
from gui.tabla import TablaEntidades
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio


class PantallaCliente(Pantalla):
    def __init__(
        self,
        parent: tk.Widget,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        pedido_servicio: PedidoServicio,
        on_cerrar_sesion: Callable[[], None],
        on_salir: Callable[[], None],
    ) -> None:
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__pedido_servicio = pedido_servicio
        super().__init__(parent, usuario, on_cerrar_sesion, on_salir)

    def _titulo(self) -> str:
        return f"Cliente - {self._usuario.nombre} {self._usuario.apellido}"

    def _construir_navegacion(self, contenedor: ttk.Frame) -> None:
        ttk.Button(contenedor, text="Ver categorías", command=self.__mostrar_categorias).pack(
            fill="x", pady=4
        )
        ttk.Button(contenedor, text="Ver productos", command=self.__mostrar_productos).pack(
            fill="x", pady=4
        )
        ttk.Button(contenedor, text="Mis pedidos", command=self.__mostrar_pedidos).pack(fill="x", pady=4)
        ttk.Button(contenedor, text="Mis datos", command=self.__mostrar_mis_datos).pack(fill="x", pady=4)

    def __mostrar_categorias(self) -> None:
        def construir(parent: tk.Widget) -> tk.Widget:
            frame = ttk.Frame(parent)
            tabla = TablaEntidades(frame, [("nombre", "Nombre", 200), ("descripcion", "Descripción", 350)])
            tabla.pack(fill="both", expand=True)
            tabla.cargar(
                [(categoria.id, (categoria.nombre, categoria.descripcion))
                 for categoria in self.__categoria_servicio.listar()]
            )
            return frame

        self._mostrar_seccion(construir)

    def __mostrar_productos(self) -> None:
        def construir(parent: tk.Widget) -> tk.Widget:
            frame = ttk.Frame(parent)
            tabla = TablaEntidades(
                frame,
                [
                    ("nombre", "Nombre", 200),
                    ("precio", "Precio", 100),
                    ("stock", "Stock", 80),
                    ("categoria", "Categoría", 150),
                ],
            )
            tabla.pack(fill="both", expand=True)
            tabla.cargar(
                [
                    (producto.id, (producto.nombre, f"${producto.precio:.2f}", producto.stock, producto.categoria.nombre))
                    for producto in self.__producto_servicio.listar_disponibles()
                ]
            )
            return frame

        self._mostrar_seccion(construir)

    def __mostrar_pedidos(self) -> None:
        def construir(parent: tk.Widget) -> tk.Widget:
            frame = ttk.Frame(parent)
            tabla = TablaEntidades(
                frame,
                [
                    ("estado", "Estado", 120),
                    ("forma_pago", "Forma de pago", 120),
                    ("total", "Total", 100),
                    ("fecha", "Fecha", 100),
                ],
            )
            tabla.pack(fill="both", expand=True)
            pedidos = self.__pedido_servicio.listar_por_usuario(self._usuario)
            tabla.cargar(
                [
                    (
                        pedido.id,
                        (pedido.estado.value, pedido.forma_pago.value, f"${pedido.total:.2f}", str(pedido.fecha)),
                    )
                    for pedido in pedidos
                ]
            )

            ttk.Label(frame, text="Detalle del pedido seleccionado:").pack(anchor="w", pady=(10, 2))
            detalle_texto = tk.Text(frame, height=8, state="disabled")
            detalle_texto.pack(fill="both", expand=True)

            def mostrar_detalle(_evento: object) -> None:
                id_pedido = tabla.id_seleccionado()
                pedido = next((pedido for pedido in pedidos if pedido.id == id_pedido), None)
                detalle_texto.config(state="normal")
                detalle_texto.delete("1.0", "end")
                if pedido is not None:
                    for detalle in pedido.detalles:
                        detalle_texto.insert("end", f"{detalle}\n")
                    detalle_texto.insert("end", f"\nTotal: ${pedido.total:.2f}")
                detalle_texto.config(state="disabled")

            tabla.bind("<<TreeviewSelect>>", mostrar_detalle)
            return frame

        self._mostrar_seccion(construir)

    def __mostrar_mis_datos(self) -> None:
        def construir(parent: tk.Widget) -> tk.Widget:
            frame = ttk.Frame(parent, padding=10)
            datos = [
                ("Nombre", self._usuario.nombre),
                ("Apellido", self._usuario.apellido),
                ("Mail", self._usuario.mail),
                ("Celular", self._usuario.celular or "-"),
                ("Rol", self._usuario.rol.value),
            ]
            for fila, (etiqueta, valor) in enumerate(datos):
                ttk.Label(frame, text=f"{etiqueta}:", font=("Segoe UI", 10, "bold")).grid(
                    row=fila, column=0, sticky="w", pady=4, padx=(0, 10)
                )
                ttk.Label(frame, text=valor).grid(row=fila, column=1, sticky="w", pady=4)
            return frame

        self._mostrar_seccion(construir)
