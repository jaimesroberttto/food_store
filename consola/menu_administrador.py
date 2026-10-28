from consola.lectura import (
    leer_confirmacion,
    leer_entero,
    leer_entero_opcional,
    leer_flotante,
    leer_flotante_opcional,
    leer_opcion_enum,
    leer_opcional,
    leer_texto,
)
from consola.menu import Menu
from entidades.categoria import Categoria
from entidades.usuario import Usuario
from enums.estado import Estado
from enums.forma_pago import FormaPago
from enums.rol import Rol
from excepciones.errores import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


class MenuAdministrador(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__usuario_servicio = usuario_servicio
        self.__pedido_servicio = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._menu_categorias()
            elif opcion == "2":
                self._menu_productos()
            elif opcion == "3":
                self._menu_usuarios()
            elif opcion == "4":
                self._menu_pedidos()
            elif opcion == "9":
                return True
            elif opcion == "0":
                return False
            else:
                print("Opción fuera de rango.")

    # ---------- Categorías ----------
    def _menu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._listar_categorias()
            elif opcion == "2":
                self._crear_categoria()
            elif opcion == "3":
                self._editar_categoria()
            elif opcion == "4":
                self._eliminar_categoria()
            elif opcion == "0":
                return
            else:
                print("Opción fuera de rango.")

    def _listar_categorias(self) -> None:
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas.")
            return
        for categoria in categorias:
            print(categoria)

    def _crear_categoria(self) -> None:
        try:
            nombre = leer_texto("Nombre: ")
            descripcion = leer_texto("Descripción: ")
            categoria = self.__categoria_servicio.crear(nombre, descripcion)
            print(f"Categoría creada con id {categoria.id}.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        try:
            id_categoria = leer_entero("Id de la categoría a editar: ")
            nombre = leer_opcional("Nuevo nombre (Enter para conservar): ")
            descripcion = leer_opcional("Nueva descripción (Enter para conservar): ")
            self.__categoria_servicio.editar(id_categoria, nombre, descripcion)
            print("Categoría actualizada.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        try:
            id_categoria = leer_entero("Id de la categoría a eliminar: ")
            categoria = self.__categoria_servicio.buscar_por_id(id_categoria)
            if not leer_confirmacion(f"¿Eliminar la categoría '{categoria.nombre}'?"):
                print("Operación cancelada.")
                return
            productos_activos = self.__producto_servicio.contar_activos_por_categoria(categoria)
            self.__categoria_servicio.eliminar(id_categoria, productos_activos)
            print("Categoría eliminada.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    # ---------- Productos ----------
    def _menu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._listar_productos()
            elif opcion == "2":
                self._crear_producto()
            elif opcion == "3":
                self._editar_producto()
            elif opcion == "4":
                self._eliminar_producto()
            elif opcion == "0":
                return
            else:
                print("Opción fuera de rango.")

    def _listar_productos(self) -> None:
        productos = self.__producto_servicio.listar()
        if not productos:
            print("No hay productos cargados.")
            return
        for producto in productos:
            print(producto)

    def _elegir_categoria(self) -> Categoria | None:
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas. Creá una primero.")
            return None
        for categoria in categorias:
            print(categoria)
        id_categoria = leer_entero("Id de la categoría: ")
        return self.__categoria_servicio.buscar_por_id(id_categoria)

    def _crear_producto(self) -> None:
        try:
            categoria = self._elegir_categoria()
            if categoria is None:
                return
            nombre = leer_texto("Nombre: ")
            descripcion = leer_texto("Descripción: ")
            precio = leer_flotante("Precio: ", minimo=0)
            stock = leer_entero("Stock: ", minimo=0)
            imagen = leer_texto("Imagen (url o nombre de archivo): ", obligatorio=False)
            disponible = leer_confirmacion("¿Disponible?")
            producto = self.__producto_servicio.crear(
                nombre, precio, descripcion, stock, imagen, disponible, categoria
            )
            print(f"Producto creado con id {producto.id}.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _editar_producto(self) -> None:
        self._listar_productos()
        try:
            id_producto = leer_entero("Id del producto a editar: ")
            nombre = leer_opcional("Nuevo nombre (Enter para conservar): ")
            descripcion = leer_opcional("Nueva descripción (Enter para conservar): ")
            precio = leer_flotante_opcional("Nuevo precio (Enter para conservar): ")
            stock = leer_entero_opcional("Nuevo stock (Enter para conservar): ")
            imagen = leer_opcional("Nueva imagen (Enter para conservar): ")
            disponible = None
            if leer_confirmacion("¿Cambiar disponibilidad?"):
                disponible = leer_confirmacion("¿Disponible?")
            self.__producto_servicio.editar(
                id_producto,
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                stock=stock,
                imagen=imagen,
                disponible=disponible,
            )
            print("Producto actualizado.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _eliminar_producto(self) -> None:
        self._listar_productos()
        try:
            id_producto = leer_entero("Id del producto a eliminar: ")
            if not leer_confirmacion("¿Confirma la eliminación?"):
                print("Operación cancelada.")
                return
            self.__producto_servicio.eliminar(id_producto)
            print("Producto eliminado.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    # ---------- Usuarios ----------
    def _menu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._listar_usuarios()
            elif opcion == "2":
                self._crear_usuario()
            elif opcion == "3":
                self._editar_usuario()
            elif opcion == "4":
                self._eliminar_usuario()
            elif opcion == "0":
                return
            else:
                print("Opción fuera de rango.")

    def _listar_usuarios(self) -> None:
        usuarios = self.__usuario_servicio.listar()
        if not usuarios:
            print("No hay usuarios cargados.")
            return
        for usuario in usuarios:
            print(usuario)

    def _crear_usuario(self) -> None:
        try:
            nombre = leer_texto("Nombre: ")
            apellido = leer_texto("Apellido: ")
            mail = leer_texto("Mail: ")
            celular = leer_texto("Celular: ", obligatorio=False)
            contrasenia = leer_texto("Contraseña: ")
            rol = leer_opcion_enum("Rol:", Rol)
            usuario = self.__usuario_servicio.crear(nombre, apellido, mail, celular, contrasenia, rol)
            print(f"Usuario creado con id {usuario.id}.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        try:
            id_usuario = leer_entero("Id del usuario a editar: ")
            nombre = leer_opcional("Nuevo nombre (Enter para conservar): ")
            apellido = leer_opcional("Nuevo apellido (Enter para conservar): ")
            mail = leer_opcional("Nuevo mail (Enter para conservar): ")
            celular = leer_opcional("Nuevo celular (Enter para conservar): ")
            self.__usuario_servicio.editar(
                id_usuario, nombre=nombre, apellido=apellido, mail=mail, celular=celular
            )
            print("Usuario actualizado.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        try:
            id_usuario = leer_entero("Id del usuario a eliminar: ")
            if not leer_confirmacion("¿Confirma la eliminación?"):
                print("Operación cancelada.")
                return
            self.__usuario_servicio.eliminar(id_usuario, self._usuario)
            print("Usuario eliminado.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    # ---------- Pedidos ----------
    def _menu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Cambiar estado / forma de pago")
            print("4. Eliminar")
            print("0. Volver")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._listar_pedidos()
            elif opcion == "2":
                self._crear_pedido()
            elif opcion == "3":
                self._actualizar_pedido()
            elif opcion == "4":
                self._eliminar_pedido()
            elif opcion == "0":
                return
            else:
                print("Opción fuera de rango.")

    def _listar_pedidos(self) -> None:
        pedidos = self.__pedido_servicio.listar()
        if not pedidos:
            print("No hay pedidos cargados.")
            return
        for pedido in pedidos:
            print(pedido)
            for detalle in pedido.detalles:
                print(f"    - {detalle}")

    def _crear_pedido(self) -> None:
        try:
            self._listar_usuarios()
            id_usuario = leer_entero("Id del usuario: ")
            usuario = self.__usuario_servicio.buscar_por_id(id_usuario)
            forma_pago = leer_opcion_enum("Forma de pago:", FormaPago)

            items = []
            while True:
                self._listar_productos()
                id_producto = leer_entero("Id del producto a agregar: ")
                producto = self.__producto_servicio.buscar_por_id(id_producto)
                cantidad = leer_entero("Cantidad: ", minimo=1)
                items.append((cantidad, producto))
                if not leer_confirmacion("¿Agregar otro producto?"):
                    break

            pedido = self.__pedido_servicio.crear(usuario, forma_pago, items)
            print(f"Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _actualizar_pedido(self) -> None:
        self._listar_pedidos()
        try:
            id_pedido = leer_entero("Id del pedido: ")
            print("1. Cambiar estado")
            print("2. Cambiar forma de pago")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                nuevo_estado = leer_opcion_enum("Nuevo estado:", Estado)
                self.__pedido_servicio.cambiar_estado(id_pedido, nuevo_estado)
                print("Estado actualizado.")
            elif opcion == "2":
                nueva_forma_pago = leer_opcion_enum("Nueva forma de pago:", FormaPago)
                self.__pedido_servicio.cambiar_forma_pago(id_pedido, nueva_forma_pago)
                print("Forma de pago actualizada.")
            else:
                print("Opción fuera de rango.")
        except FoodStoreError as error:
            print(f"Error: {error}")

    def _eliminar_pedido(self) -> None:
        self._listar_pedidos()
        try:
            id_pedido = leer_entero("Id del pedido a eliminar: ")
            if not leer_confirmacion("¿Confirma la eliminación?"):
                print("Operación cancelada.")
                return
            self.__pedido_servicio.eliminar(id_pedido)
            print("Pedido eliminado.")
        except FoodStoreError as error:
            print(f"Error: {error}")
