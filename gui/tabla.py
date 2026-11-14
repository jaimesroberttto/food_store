"""Treeview reutilizable para listar entidades con columnas fijas."""

import tkinter as tk
from tkinter import ttk
from typing import Any


class TablaEntidades(ttk.Treeview):
    def __init__(self, parent: tk.Widget, columnas: list[tuple[str, str, int]]) -> None:
        claves = [clave for clave, _titulo, _ancho in columnas]
        super().__init__(parent, columns=claves, show="headings", selectmode="browse")
        for clave, titulo, ancho in columnas:
            self.heading(clave, text=titulo)
            self.column(clave, width=ancho, anchor="w")
        self.__ids: dict[str, Any] = {}

    def cargar(self, filas: list[tuple[Any, tuple]]) -> None:
        """filas: lista de (id_entidad, valores_de_columna)."""
        self.delete(*self.get_children())
        self.__ids.clear()
        for id_entidad, valores in filas:
            item = self.insert("", "end", values=valores)
            self.__ids[item] = id_entidad

    def id_seleccionado(self) -> Any | None:
        seleccion = self.selection()
        if not seleccion:
            return None
        return self.__ids.get(seleccion[0])
