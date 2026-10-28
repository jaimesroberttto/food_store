from abc import ABC, abstractmethod
from datetime import datetime


class Base(ABC):
    """Superclase de todas las entidades: id autogenerado, baja lógica y fecha de alta."""

    _contador_id: int = 0

    def __init__(self) -> None:
        Base._contador_id += 1
        self.__id: int = Base._contador_id
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, valor: bool) -> None:
        self.__eliminado = bool(valor)

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Base):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @abstractmethod
    def __str__(self) -> str:
        ...
