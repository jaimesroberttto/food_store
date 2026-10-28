from consola.lectura import leer_entero, leer_texto
from consola.menu import Menu
from entidades.usuario import Usuario
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio


class MenuCliente(Menu):
    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        pedido_servicio: PedidoServicio,
    ) -> None:
        super().__init__(usuario)
        self.__categoria_servicio = categoria_servicio
        self.__producto_servicio = producto_servicio
        self.__pedido_servicio = pedido_servicio

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = leer_texto("Seleccione: ", obligatorio=False)
            if opcion == "1":
                self._ver_categorias()
            elif opcion == "2":
                self._ver_productos()
            elif opcion == "3":
                self._ver_mis_pedidos()
            elif opcion == "4":
                self._ver_mis_datos()
            elif opcion == "9":
                return True
            elif opcion == "0":
                return False
            else:
                print("Opción fuera de rango.")

    def _ver_categorias(self) -> None:
        categorias = self.__categoria_servicio.listar()
        if not categorias:
            print("No hay categorías cargadas.")
            return
        for categoria in categorias:
            print(categoria)

    def _ver_productos(self) -> None:
        productos = self.__producto_servicio.listar_disponibles()
        if not productos:
            print("No hay productos disponibles.")
            return
        for producto in productos:
            print(producto)

    def _ver_mis_pedidos(self) -> None:
        pedidos = self.__pedido_servicio.listar_por_usuario(self._usuario)
        if not pedidos:
            print("No tenés pedidos registrados.")
            return
        for pedido in pedidos:
            print(pedido)
        id_pedido = leer_entero("Id de pedido a consultar (0 para volver): ", minimo=0)
        if id_pedido == 0:
            return
        pedido_elegido = next((pedido for pedido in pedidos if pedido.id == id_pedido), None)
        if pedido_elegido is None:
            print("No existe ese pedido.")
            return
        for detalle in pedido_elegido.detalles:
            print(f"    - {detalle}")
        print(f"Total: ${pedido_elegido.total:.2f}")

    def _ver_mis_datos(self) -> None:
        print(self._usuario)
