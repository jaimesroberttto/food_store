"""Formulario modal genérico: arma un Toplevel con campos y devuelve los valores cargados."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class Formulario(tk.Toplevel):
    def __init__(self, parent: tk.Widget, titulo: str) -> None:
        super().__init__(parent)
        self.title(titulo)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.aceptado: bool = False
        self.__fila: int = 0
        self.__variables: dict[str, tk.Variable] = {}
        self.__combos_objeto: dict[str, dict[str, Any]] = {}

        self.__cuerpo = ttk.Frame(self, padding=15)
        self.__cuerpo.pack(fill="both", expand=True)
        self.__cuerpo.grid_columnconfigure(1, weight=1)

    def agregar_texto(self, clave: str, etiqueta: str, valor_inicial: str = "", oculto: bool = False) -> None:
        variable = tk.StringVar(value=valor_inicial)
        self.__agregar_etiqueta(etiqueta)
        entrada = ttk.Entry(self.__cuerpo, textvariable=variable, width=30, show="*" if oculto else "")
        entrada.grid(row=self.__fila, column=1, sticky="we", pady=4)
        self.__variables[clave] = variable
        self.__fila += 1

    def agregar_combobox(self, clave: str, etiqueta: str, opciones: list[str], valor_inicial: str = "") -> None:
        variable = tk.StringVar(value=valor_inicial)
        self.__agregar_etiqueta(etiqueta)
        combo = ttk.Combobox(
            self.__cuerpo, textvariable=variable, values=opciones, state="readonly", width=28
        )
        combo.grid(row=self.__fila, column=1, sticky="we", pady=4)
        self.__variables[clave] = variable
        self.__fila += 1

    def agregar_combobox_objetos(
        self,
        clave: str,
        etiqueta: str,
        objetos: list[T],
        texto: Callable[[T], str],
        valor_inicial: T | None = None,
    ) -> None:
        etiquetas = [texto(objeto) for objeto in objetos]
        mapa = dict(zip(etiquetas, objetos))
        variable = tk.StringVar(value=texto(valor_inicial) if valor_inicial is not None else "")
        self.__agregar_etiqueta(etiqueta)
        combo = ttk.Combobox(
            self.__cuerpo, textvariable=variable, values=etiquetas, state="readonly", width=28
        )
        combo.grid(row=self.__fila, column=1, sticky="we", pady=4)
        self.__variables[clave] = variable
        self.__combos_objeto[clave] = mapa
        self.__fila += 1

    def agregar_booleano(self, clave: str, etiqueta: str, valor_inicial: bool = False) -> None:
        variable = tk.BooleanVar(value=valor_inicial)
        check = ttk.Checkbutton(self.__cuerpo, text=etiqueta, variable=variable)
        check.grid(row=self.__fila, column=1, sticky="w", pady=4)
        self.__variables[clave] = variable
        self.__fila += 1

    def agregar_botones(self, texto_aceptar: str = "Aceptar") -> None:
        barra = ttk.Frame(self.__cuerpo)
        barra.grid(row=self.__fila, column=0, columnspan=2, pady=(15, 0), sticky="e")
        ttk.Button(barra, text="Cancelar", command=self.__cancelar).pack(side="right", padx=4)
        ttk.Button(barra, text=texto_aceptar, command=self.__aceptar).pack(side="right")
        self.__fila += 1

    def __agregar_etiqueta(self, etiqueta: str) -> None:
        ttk.Label(self.__cuerpo, text=etiqueta).grid(row=self.__fila, column=0, sticky="w", padx=(0, 10), pady=4)

    def __aceptar(self) -> None:
        self.aceptado = True
        self.destroy()

    def __cancelar(self) -> None:
        self.aceptado = False
        self.destroy()

    def texto(self, clave: str) -> str:
        return str(self.__variables[clave].get()).strip()

    def booleano(self, clave: str) -> bool:
        return bool(self.__variables[clave].get())

    def objeto(self, clave: str) -> Any:
        etiqueta = self.__variables[clave].get()
        return self.__combos_objeto[clave].get(etiqueta)

    def esperar(self) -> bool:
        self.wait_window()
        return self.aceptado
