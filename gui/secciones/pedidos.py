"""Sección de administración de pedidos: listar, crear con detalles, cambiar estado/forma de pago y eliminar."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from entidades.producto import Producto
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.errores import FoodStoreError
from gui.dialogos import confirmar, mostrar_error, mostrar_info
from gui.formularios import Formulario
from gui.tabla import TablaEntidades
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def _texto_usuario(usuario: Usuario) -> str:
    return f"{usuario.id} - {usuario.nombre} {usuario.apellido}"


def _texto_producto(producto: Producto) -> str:
    return f"{producto.id} - {producto.nombre} (stock: {producto.stock})"


class SeccionPedidos(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        pedido_servicio: PedidoServicio,
        usuario_servicio: UsuarioServicio,
        producto_servicio: ProductoServicio,
    ) -> None:
        super().__init__(parent)
        self.__pedido_servicio = pedido_servicio
        self.__usuario_servicio = usuario_servicio
        self.__producto_servicio = producto_servicio

        ttk.Label(self, text="Pedidos", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        barra_botones = ttk.Frame(self)
        barra_botones.pack(fill="x", pady=(5, 10))
        ttk.Button(barra_botones, text="Actualizar", command=self.__refrescar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Crear", command=self.__crear).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Ver detalle", command=self.__ver_detalle).pack(side="left", padx=2)
        ttk.Button(
            barra_botones, text="Cambiar estado/forma de pago", command=self.__actualizar
        ).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Eliminar", command=self.__eliminar).pack(side="left", padx=2)

        self.__tabla = TablaEntidades(
            self,
            [
                ("usuario", "Usuario", 160),
                ("estado", "Estado", 110),
                ("forma_pago", "Forma de pago", 120),
                ("total", "Total", 90),
                ("fecha", "Fecha", 100),
            ],
        )
        self.__tabla.pack(fill="both", expand=True)
        self.__tabla.bind("<Double-1>", lambda evento: self.__ver_detalle())

        self.__refrescar()

    def __refrescar(self) -> None:
        pedidos = self.__pedido_servicio.listar()
        self.__tabla.cargar(
            [
                (
                    pedido.id,
                    (
                        f"{pedido.usuario.nombre} {pedido.usuario.apellido}",
                        pedido.estado.value,
                        pedido.forma_pago.value,
                        f"${pedido.total:.2f}",
                        str(pedido.fecha),
                    ),
                )
                for pedido in pedidos
            ]
        )

    def __ver_detalle(self) -> None:
        id_pedido = self.__tabla.id_seleccionado()
        if id_pedido is None:
            mostrar_error("Seleccioná un pedido de la lista.")
            return
        pedido = self.__pedido_servicio.buscar_por_id(id_pedido)
        ventana = tk.Toplevel(self)
        ventana.title(f"Detalle del pedido {pedido.id}")
        texto = tk.Text(ventana, width=50, height=10)
        texto.pack(padx=10, pady=10, fill="both", expand=True)
        for detalle in pedido.detalles:
            texto.insert("end", f"{detalle}\n")
        texto.insert("end", f"\nTotal: ${pedido.total:.2f}")
        texto.config(state="disabled")

    def __crear(self) -> None:
        usuarios = self.__usuario_servicio.listar()
        if not usuarios:
            mostrar_error("No hay usuarios cargados. Creá uno primero.")
            return
        productos = self.__producto_servicio.listar()
        if not productos:
            mostrar_error("No hay productos cargados. Creá uno primero.")
            return
        _DialogoCrearPedido(self, usuarios, productos, self.__pedido_servicio, self.__refrescar).esperar()

    def __actualizar(self) -> None:
        id_pedido = self.__tabla.id_seleccionado()
        if id_pedido is None:
            mostrar_error("Seleccioná un pedido de la lista.")
            return
        pedido = self.__pedido_servicio.buscar_por_id(id_pedido)

        formulario = Formulario(self, f"Pedido {pedido.id}")
        formulario.agregar_combobox(
            "estado", "Nuevo estado:", [estado.value for estado in Estado], pedido.estado.value
        )
        formulario.agregar_combobox(
            "forma_pago", "Nueva forma de pago:", [fp.value for fp in FormaPago], pedido.forma_pago.value
        )
        formulario.agregar_botones("Guardar")
        if not formulario.esperar():
            return
        try:
            nuevo_estado = Estado(formulario.texto("estado"))
            if nuevo_estado != pedido.estado:
                self.__pedido_servicio.cambiar_estado(id_pedido, nuevo_estado)
            nueva_forma_pago = FormaPago(formulario.texto("forma_pago"))
            if nueva_forma_pago != pedido.forma_pago:
                self.__pedido_servicio.cambiar_forma_pago(id_pedido, nueva_forma_pago)
            mostrar_info("Pedido actualizado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __eliminar(self) -> None:
        id_pedido = self.__tabla.id_seleccionado()
        if id_pedido is None:
            mostrar_error("Seleccioná un pedido de la lista.")
            return
        if not confirmar("¿Confirma la eliminación del pedido?"):
            return
        try:
            self.__pedido_servicio.eliminar(id_pedido)
            mostrar_info("Pedido eliminado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))


class _DialogoCrearPedido(tk.Toplevel):
    """Arma un pedido agregando ítems en memoria y recién lo confirma con PedidoServicio.crear."""

    def __init__(
        self,
        parent: tk.Widget,
        usuarios: list[Usuario],
        productos: list[Producto],
        pedido_servicio: PedidoServicio,
        on_creado: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self.title("Nuevo pedido")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.__pedido_servicio = pedido_servicio
        self.__on_creado = on_creado
        self.__usuarios_por_texto = {_texto_usuario(usuario): usuario for usuario in usuarios}
        self.__productos_por_texto = {_texto_producto(producto): producto for producto in productos}
        self.__items: dict[int, tuple[Producto, int]] = {}

        cuerpo = ttk.Frame(self, padding=15)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)

        ttk.Label(cuerpo, text="Usuario:").grid(row=0, column=0, sticky="w", pady=4)
        self.__usuario_var = tk.StringVar()
        ttk.Combobox(
            cuerpo,
            textvariable=self.__usuario_var,
            values=list(self.__usuarios_por_texto.keys()),
            state="readonly",
            width=35,
        ).grid(row=0, column=1, columnspan=3, sticky="we", pady=4)

        ttk.Label(cuerpo, text="Forma de pago:").grid(row=1, column=0, sticky="w", pady=4)
        self.__forma_pago_var = tk.StringVar(value=FormaPago.EFECTIVO.value)
        ttk.Combobox(
            cuerpo,
            textvariable=self.__forma_pago_var,
            values=[fp.value for fp in FormaPago],
            state="readonly",
            width=35,
        ).grid(row=1, column=1, columnspan=3, sticky="we", pady=4)

        ttk.Separator(cuerpo).grid(row=2, column=0, columnspan=4, sticky="we", pady=10)

        ttk.Label(cuerpo, text="Producto:").grid(row=3, column=0, sticky="w", pady=4)
        self.__producto_var = tk.StringVar()
        ttk.Combobox(
            cuerpo,
            textvariable=self.__producto_var,
            values=list(self.__productos_por_texto.keys()),
            state="readonly",
            width=35,
        ).grid(row=3, column=1, columnspan=3, sticky="we", pady=4)

        ttk.Label(cuerpo, text="Cantidad:").grid(row=4, column=0, sticky="w", pady=4)
        self.__cantidad_var = tk.StringVar(value="1")
        ttk.Entry(cuerpo, textvariable=self.__cantidad_var, width=10).grid(row=4, column=1, sticky="w", pady=4)
        ttk.Button(cuerpo, text="Agregar ítem", command=self.__agregar_item).grid(row=4, column=2, padx=5)
        ttk.Button(cuerpo, text="Quitar ítem", command=self.__quitar_item).grid(row=4, column=3)

        self.__tabla_items = TablaEntidades(
            cuerpo, [("producto", "Producto", 220), ("cantidad", "Cantidad", 80)]
        )
        self.__tabla_items.grid(row=5, column=0, columnspan=4, sticky="nswe", pady=10)
        cuerpo.grid_rowconfigure(5, weight=1)

        barra = ttk.Frame(cuerpo)
        barra.grid(row=6, column=0, columnspan=4, sticky="e")
        ttk.Button(barra, text="Cancelar", command=self.destroy).pack(side="right", padx=4)
        ttk.Button(barra, text="Crear pedido", command=self.__confirmar).pack(side="right")

    def __agregar_item(self) -> None:
        producto = self.__productos_por_texto.get(self.__producto_var.get())
        if producto is None:
            mostrar_error("Seleccioná un producto.")
            return
        try:
            cantidad = int(self.__cantidad_var.get())
        except ValueError:
            mostrar_error("La cantidad debe ser un número entero.")
            return
        if cantidad <= 0:
            mostrar_error("La cantidad debe ser mayor a 0.")
            return
        cantidad_previa = self.__items.get(producto.id, (producto, 0))[1]
        self.__items[producto.id] = (producto, cantidad_previa + cantidad)
        self.__refrescar_items()

    def __quitar_item(self) -> None:
        id_producto = self.__tabla_items.id_seleccionado()
        if id_producto is None:
            mostrar_error("Seleccioná un ítem de la lista para quitarlo.")
            return
        self.__items.pop(id_producto, None)
        self.__refrescar_items()

    def __refrescar_items(self) -> None:
        self.__tabla_items.cargar(
            [(producto.id, (producto.nombre, cantidad)) for producto, cantidad in self.__items.values()]
        )

    def __confirmar(self) -> None:
        usuario = self.__usuarios_por_texto.get(self.__usuario_var.get())
        if usuario is None:
            mostrar_error("Seleccioná un usuario.")
            return
        if not self.__items:
            mostrar_error("Agregá al menos un producto al pedido.")
            return
        items = [(cantidad, producto) for producto, cantidad in self.__items.values()]
        try:
            pedido = self.__pedido_servicio.crear(usuario, FormaPago(self.__forma_pago_var.get()), items)
            mostrar_info(f"Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")
            self.__on_creado()
            self.destroy()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def esperar(self) -> None:
        self.wait_window()
