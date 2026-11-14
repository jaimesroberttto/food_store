"""Sección de administración de categorías: listar, crear, editar y eliminar."""

import tkinter as tk
from tkinter import ttk

from excepciones.errores import FoodStoreError
from gui.dialogos import confirmar, mostrar_error, mostrar_info
from gui.formularios import Formulario
from gui.tabla import TablaEntidades
from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio


class SeccionCategorias(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
    ) -> None:
        super().__init__(parent)
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio

        ttk.Label(self, text="Categorías", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        barra_botones = ttk.Frame(self)
        barra_botones.pack(fill="x", pady=(5, 10))
        ttk.Button(barra_botones, text="Actualizar", command=self.__refrescar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Crear", command=self.__crear).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Editar", command=self.__editar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Eliminar", command=self.__eliminar).pack(side="left", padx=2)

        self.__tabla = TablaEntidades(
            self, [("nombre", "Nombre", 200), ("descripcion", "Descripción", 400)]
        )
        self.__tabla.pack(fill="both", expand=True)

        self.__refrescar()

    def __refrescar(self) -> None:
        categorias = self.__categoria_servicio.listar()
        self.__tabla.cargar([(categoria.id, (categoria.nombre, categoria.descripcion)) for categoria in categorias])

    def __crear(self) -> None:
        formulario = Formulario(self, "Nueva categoría")
        formulario.agregar_texto("nombre", "Nombre:")
        formulario.agregar_texto("descripcion", "Descripción:")
        formulario.agregar_botones("Crear")
        if not formulario.esperar():
            return
        try:
            categoria = self.__categoria_servicio.crear(formulario.texto("nombre"), formulario.texto("descripcion"))
            mostrar_info(f"Categoría creada con id {categoria.id}.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __editar(self) -> None:
        id_categoria = self.__tabla.id_seleccionado()
        if id_categoria is None:
            mostrar_error("Seleccioná una categoría de la lista.")
            return
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
        formulario = Formulario(self, "Editar categoría")
        formulario.agregar_texto("nombre", "Nombre:", categoria.nombre)
        formulario.agregar_texto("descripcion", "Descripción:", categoria.descripcion)
        formulario.agregar_botones("Guardar")
        if not formulario.esperar():
            return
        try:
            self.__categoria_servicio.editar(
                id_categoria, formulario.texto("nombre") or None, formulario.texto("descripcion") or None
            )
            mostrar_info("Categoría actualizada.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __eliminar(self) -> None:
        id_categoria = self.__tabla.id_seleccionado()
        if id_categoria is None:
            mostrar_error("Seleccioná una categoría de la lista.")
            return
        categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
        if not confirmar(f"¿Eliminar la categoría '{categoria.nombre}'?"):
            return
        try:
            productos_activos = self.__producto_servicio.contar_activos_por_categoria(categoria)
            self.__categoria_servicio.eliminar(id_categoria, productos_activos)
            mostrar_info("Categoría eliminada.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))
