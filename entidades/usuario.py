from entidades.base import Base
from enums.rol import Rol
from excepciones.errores import DatoInvalidoError


class Usuario(Base):
    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia = self._validar_contrasenia(contrasenia)
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail no tiene un formato válido")
        self.__mail = valor.strip().lower()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = valor.strip() if valor else ""

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol no es válido")
        self.__rol = valor

    @staticmethod
    def _validar_contrasenia(valor: str) -> str:
        if not valor or len(valor.strip()) < 4:
            raise DatoInvalidoError("La contraseña debe tener al menos 4 caracteres")
        return valor.strip()

    def cambiar_contrasenia(self, nueva_contrasenia: str) -> None:
        self.__contrasenia = self._validar_contrasenia(nueva_contrasenia)

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} {self.apellido} - {self.mail} - {self.rol.value}"
