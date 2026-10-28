from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.errores import (
    CredencialesInvalidasError,
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)


class UsuarioServicio:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def listar(self) -> list[Usuario]:
        return [usuario for usuario in self.__usuarios if not usuario.eliminado]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(f"No existe el usuario con id {id_usuario}")

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        self._validar_mail_unico(mail)
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(usuario)
        return usuario

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)
        if nombre:
            usuario.nombre = nombre
        if apellido:
            usuario.apellido = apellido
        if mail:
            self._validar_mail_unico(mail, ignorar_id=id_usuario)
            usuario.mail = mail
        if celular is not None:
            usuario.celular = celular
        if rol is not None:
            usuario.rol = rol
        return usuario

    def eliminar(self, id_usuario: int, usuario_en_sesion: Usuario) -> Usuario:
        if id_usuario == usuario_en_sesion.id:
            raise OperacionNoPermitidaError(
                "No podés eliminarte a vos mismo mientras tenés la sesión iniciada"
            )
        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminado = True
        return usuario

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        mail_normalizado = mail.strip().lower()
        for usuario in self.__usuarios:
            if usuario.mail == mail_normalizado and not usuario.eliminado:
                if usuario.verificar_contrasenia(contrasenia):
                    return usuario
                raise CredencialesInvalidasError("Mail o contraseña incorrectos")
        raise CredencialesInvalidasError("Mail o contraseña incorrectos")

    def _validar_mail_unico(self, mail: str, ignorar_id: int | None = None) -> None:
        mail_normalizado = mail.strip().lower()
        for usuario in self.__usuarios:
            if usuario.eliminado or usuario.id == ignorar_id:
                continue
            if usuario.mail == mail_normalizado:
                raise DuplicadoError(f"Ya existe un usuario con el mail '{mail}'")
