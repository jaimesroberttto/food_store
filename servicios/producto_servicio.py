from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.errores import EntidadNoEncontradaError


class ProductoServicio:
    def __init__(self) -> None:
        self.__productos: list[Producto] = []

    def listar(self) -> list[Producto]:
        return [producto for producto in self.__productos if not producto.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        return [producto for producto in self.listar() if producto.disponible and producto.stock > 0]

    def listar_por_categoria(self, categoria: Categoria) -> list[Producto]:
        return [producto for producto in self.listar() if producto.categoria == categoria]

    def contar_activos_por_categoria(self, categoria: Categoria) -> int:
        return len(self.listar_por_categoria(categoria))

    def buscar_por_id(self, id_producto: int) -> Producto:
        for producto in self.__productos:
            if producto.id == id_producto and not producto.eliminado:
                return producto
        raise EntidadNoEncontradaError(f"No existe el producto con id {id_producto}")

    def crear(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> Producto:
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    def editar(
        self,
        id_producto: int,
        nombre: str | None = None,
        precio: float | None = None,
        descripcion: str | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        categoria: Categoria | None = None,
    ) -> Producto:
        producto = self.buscar_por_id(id_producto)
        if nombre:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if descripcion is not None:
            producto.descripcion = descripcion
        if stock is not None:
            producto.stock = stock
        if imagen is not None:
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        if categoria is not None:
            producto.categoria = categoria
        return producto

    def eliminar(self, id_producto: int) -> Producto:
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True
        return producto

    def descontar_stock(self, producto: Producto, cantidad: int) -> None:
        producto.stock = producto.stock - cantidad

    def devolver_stock(self, producto: Producto, cantidad: int) -> None:
        producto.stock = producto.stock + cantidad
