"""Pantalla de inicio de sesión: pide mail y contraseña, con hasta 3 intentos."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from entidades.usuario import Usuario
from excepciones.errores import CredencialesInvalidasError
from gui.dialogos import mostrar_error
from servicios.usuario_servicio import UsuarioServicio

MAX_INTENTOS_LOGIN = 3


class PantallaLogin(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        usuario_servicio: UsuarioServicio,
        on_login_exitoso: Callable[[Usuario], None],
        on_intentos_agotados: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=30)
        self.__usuario_servicio = usuario_servicio
        self.__on_login_exitoso = on_login_exitoso
        self.__on_intentos_agotados = on_intentos_agotados
        self.__intentos_restantes = MAX_INTENTOS_LOGIN

        self.__mail = tk.StringVar()
        self.__contrasenia = tk.StringVar()

        contenedor = ttk.Frame(self)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(contenedor, text="FOOD STORE", font=("Segoe UI", 20, "bold")).pack(pady=(0, 5))
        ttk.Label(contenedor, text="Inicio de sesión", font=("Segoe UI", 12)).pack(pady=(0, 20))

        formulario = ttk.Frame(contenedor)
        formulario.pack()
        ttk.Label(formulario, text="Mail:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(formulario, textvariable=self.__mail, width=30).grid(row=0, column=1, pady=4)
        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(formulario, textvariable=self.__contrasenia, show="*", width=30).grid(
            row=1, column=1, pady=4
        )

        self.__etiqueta_estado = ttk.Label(contenedor, text="", foreground="#b00020")
        self.__etiqueta_estado.pack(pady=(10, 0))

        ttk.Button(contenedor, text="Ingresar", command=self.__intentar_login).pack(pady=15)

        self.bind_all("<Return>", lambda evento: self.__intentar_login())

    def __intentar_login(self) -> None:
        mail = self.__mail.get().strip()
        contrasenia = self.__contrasenia.get()
        try:
            usuario = self.__usuario_servicio.autenticar(mail, contrasenia)
        except CredencialesInvalidasError as error:
            self.__intentos_restantes -= 1
            if self.__intentos_restantes > 0:
                self.__etiqueta_estado.config(
                    text=f"{error}. Intentos restantes: {self.__intentos_restantes}"
                )
                self.__contrasenia.set("")
            else:
                self.unbind_all("<Return>")
                mostrar_error(f"{error}. Se agotaron los intentos de inicio de sesión.")
                self.__on_intentos_agotados()
            return
        self.unbind_all("<Return>")
        self.__on_login_exitoso(usuario)
