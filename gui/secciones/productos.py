"""Sección de administración de productos: listar, crear, editar y eliminar."""

import tkinter as tk
from tkinter import ttk

from entidades.categoria import Categoria
from excepciones.errores import FoodStoreError
from gui.dialogos import confirmar, mostrar_error, mostrar_info
from gui.formularios import Formulario
from gui.tabla import TablaEntidades
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio


def _texto_categoria(categoria: Categoria) -> str:
    return f"{categoria.id} - {categoria.nombre}"


class SeccionProductos(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        producto_servicio: ProductoServicio,
        categoria_servicio: CategoriaServicio,
    ) -> None:
        super().__init__(parent)
        self.__producto_servicio = producto_servicio
        self.__categoria_servicio = categoria_servicio

        ttk.Label(self, text="Productos", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        barra_botones = ttk.Frame(self)
        barra_botones.pack(fill="x", pady=(5, 10))
        ttk.Button(barra_botones, text="Actualizar", command=self.__refrescar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Crear", command=self.__crear).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Editar", command=self.__editar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Eliminar", command=self.__eliminar).pack(side="left", padx=2)

        self.__tabla = TablaEntidades(
            self,
            [
                ("nombre", "Nombre", 180),
                ("precio", "Precio", 90),
                ("stock", "Stock", 70),
                ("categoria", "Categoría", 140),
                ("disponible", "Disponible", 90),
            ],
        )
        self.__tabla.pack(fill="both", expand=True)

        self.__refrescar()

    def __refrescar(self) -> None:
        productos = self.__producto_servicio.listar()
        self.__tabla.cargar(
            [
                (
                    producto.id,
                    (
                        producto.nombre,
                        f"${producto.precio:.2f}",
                        producto.stock,
                        producto.categoria.nombre,
                        "Sí" if producto.disponible else "No",
                    ),
                )
                for producto in productos
            ]
        )

    def __crear(self) -> None:
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            mostrar_error("No hay categorías cargadas. Creá una primero.")
            return
        formulario = Formulario(self, "Nuevo producto")
        formulario.agregar_texto("nombre", "Nombre:")
        formulario.agregar_texto("descripcion", "Descripción:")
        formulario.agregar_texto("precio", "Precio:")
        formulario.agregar_texto("stock", "Stock:")
        formulario.agregar_texto("imagen", "Imagen (url o archivo):")
        formulario.agregar_booleano("disponible", "Disponible", True)
        formulario.agregar_combobox_objetos("categoria", "Categoría:", categorias, _texto_categoria)
        formulario.agregar_botones("Crear")
        if not formulario.esperar():
            return
        try:
            precio = float(formulario.texto("precio"))
            stock = int(formulario.texto("stock"))
        except ValueError:
            mostrar_error("Precio y stock deben ser números válidos.")
            return
        categoria = formulario.objeto("categoria")
        if categoria is None:
            mostrar_error("Seleccioná una categoría.")
            return
        try:
            producto = self.__producto_servicio.crear(
                formulario.texto("nombre"),
                precio,
                formulario.texto("descripcion"),
                stock,
                formulario.texto("imagen"),
                formulario.booleano("disponible"),
                categoria,
            )
            mostrar_info(f"Producto creado con id {producto.id}.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __editar(self) -> None:
        id_producto = self.__tabla.id_seleccionado()
        if id_producto is None:
            mostrar_error("Seleccioná un producto de la lista.")
            return
        producto = self.__producto_servicio.buscar_por_id(id_producto)
        categorias = self.__categoria_servicio.listar()
        formulario = Formulario(self, "Editar producto")
        formulario.agregar_texto("nombre", "Nombre:", producto.nombre)
        formulario.agregar_texto("descripcion", "Descripción:", producto.descripcion)
        formulario.agregar_texto("precio", "Precio:", str(producto.precio))
        formulario.agregar_texto("stock", "Stock:", str(producto.stock))
        formulario.agregar_texto("imagen", "Imagen:", producto.imagen)
        formulario.agregar_booleano("disponible", "Disponible", producto.disponible)
        formulario.agregar_combobox_objetos(
            "categoria", "Categoría:", categorias, _texto_categoria, producto.categoria
        )
        formulario.agregar_botones("Guardar")
        if not formulario.esperar():
            return
        try:
            precio = float(formulario.texto("precio"))
            stock = int(formulario.texto("stock"))
        except ValueError:
            mostrar_error("Precio y stock deben ser números válidos.")
            return
        try:
            self.__producto_servicio.editar(
                id_producto,
                nombre=formulario.texto("nombre"),
                precio=precio,
                descripcion=formulario.texto("descripcion"),
                stock=stock,
                imagen=formulario.texto("imagen"),
                disponible=formulario.booleano("disponible"),
                categoria=formulario.objeto("categoria"),
            )
            mostrar_info("Producto actualizado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __eliminar(self) -> None:
        id_producto = self.__tabla.id_seleccionado()
        if id_producto is None:
            mostrar_error("Seleccioná un producto de la lista.")
            return
        if not confirmar("¿Confirma la eliminación del producto?"):
            return
        try:
            self.__producto_servicio.eliminar(id_producto)
            mostrar_info("Producto eliminado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))
