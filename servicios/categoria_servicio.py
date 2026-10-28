from entidades.categoria import Categoria
from excepciones.errores import (
    DuplicadoError,
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
)


class CategoriaServicio:
    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]:
        return [categoria for categoria in self.__categorias if not categoria.eliminado]

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(f"No existe la categoría con id {id_categoria}")

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        self._validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def editar(
        self, id_categoria: int, nombre: str | None, descripcion: str | None
    ) -> Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if nombre:
            self._validar_nombre_unico(nombre, ignorar_id=id_categoria)
            categoria.nombre = nombre
        if descripcion:
            categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int, productos_activos: int) -> Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if productos_activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar: la categoría tiene {productos_activos} producto(s) activo(s)"
            )
        categoria.eliminado = True
        return categoria

    def _validar_nombre_unico(self, nombre: str, ignorar_id: int | None = None) -> None:
        nombre_normalizado = nombre.strip().lower()
        for categoria in self.__categorias:
            if categoria.eliminado or categoria.id == ignorar_id:
                continue
            if categoria.nombre.lower() == nombre_normalizado:
                raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'")
