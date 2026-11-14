"""Sección de administración de usuarios: listar, crear, editar y eliminar."""

import tkinter as tk
from tkinter import ttk

from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.errores import FoodStoreError
from gui.dialogos import confirmar, mostrar_error, mostrar_info
from gui.formularios import Formulario
from gui.tabla import TablaEntidades
from servicios.usuario_servicio import UsuarioServicio


class SeccionUsuarios(ttk.Frame):
    def __init__(
        self, parent: tk.Widget, usuario_servicio: UsuarioServicio, usuario_en_sesion: Usuario
    ) -> None:
        super().__init__(parent)
        self.__usuario_servicio = usuario_servicio
        self.__usuario_en_sesion = usuario_en_sesion

        ttk.Label(self, text="Usuarios", font=("Segoe UI", 13, "bold")).pack(anchor="w")

        barra_botones = ttk.Frame(self)
        barra_botones.pack(fill="x", pady=(5, 10))
        ttk.Button(barra_botones, text="Actualizar", command=self.__refrescar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Crear", command=self.__crear).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Editar", command=self.__editar).pack(side="left", padx=2)
        ttk.Button(barra_botones, text="Eliminar", command=self.__eliminar).pack(side="left", padx=2)

        self.__tabla = TablaEntidades(
            self,
            [
                ("nombre", "Nombre", 120),
                ("apellido", "Apellido", 120),
                ("mail", "Mail", 220),
                ("rol", "Rol", 90),
            ],
        )
        self.__tabla.pack(fill="both", expand=True)

        self.__refrescar()

    def __refrescar(self) -> None:
        usuarios = self.__usuario_servicio.listar()
        self.__tabla.cargar(
            [(usuario.id, (usuario.nombre, usuario.apellido, usuario.mail, usuario.rol.value)) for usuario in usuarios]
        )

    def __crear(self) -> None:
        formulario = Formulario(self, "Nuevo usuario")
        formulario.agregar_texto("nombre", "Nombre:")
        formulario.agregar_texto("apellido", "Apellido:")
        formulario.agregar_texto("mail", "Mail:")
        formulario.agregar_texto("celular", "Celular:")
        formulario.agregar_texto("contrasenia", "Contraseña:", oculto=True)
        formulario.agregar_combobox("rol", "Rol:", [rol.value for rol in Rol], Rol.USUARIO.value)
        formulario.agregar_botones("Crear")
        if not formulario.esperar():
            return
        try:
            usuario = self.__usuario_servicio.crear(
                formulario.texto("nombre"),
                formulario.texto("apellido"),
                formulario.texto("mail"),
                formulario.texto("celular"),
                formulario.texto("contrasenia"),
                Rol(formulario.texto("rol")),
            )
            mostrar_info(f"Usuario creado con id {usuario.id}.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __editar(self) -> None:
        id_usuario = self.__tabla.id_seleccionado()
        if id_usuario is None:
            mostrar_error("Seleccioná un usuario de la lista.")
            return
        usuario = self.__usuario_servicio.buscar_por_id(id_usuario)
        formulario = Formulario(self, "Editar usuario")
        formulario.agregar_texto("nombre", "Nombre:", usuario.nombre)
        formulario.agregar_texto("apellido", "Apellido:", usuario.apellido)
        formulario.agregar_texto("mail", "Mail:", usuario.mail)
        formulario.agregar_texto("celular", "Celular:", usuario.celular)
        formulario.agregar_botones("Guardar")
        if not formulario.esperar():
            return
        try:
            self.__usuario_servicio.editar(
                id_usuario,
                nombre=formulario.texto("nombre") or None,
                apellido=formulario.texto("apellido") or None,
                mail=formulario.texto("mail") or None,
                celular=formulario.texto("celular") or None,
            )
            mostrar_info("Usuario actualizado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))

    def __eliminar(self) -> None:
        id_usuario = self.__tabla.id_seleccionado()
        if id_usuario is None:
            mostrar_error("Seleccioná un usuario de la lista.")
            return
        if not confirmar("¿Confirma la eliminación del usuario?"):
            return
        try:
            self.__usuario_servicio.eliminar(id_usuario, self.__usuario_en_sesion)
            mostrar_info("Usuario eliminado.")
            self.__refrescar()
        except FoodStoreError as error:
            mostrar_error(str(error))
