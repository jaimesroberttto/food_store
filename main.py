from consola.fabrica import crear_menu
from consola.lectura import leer_texto
from enums.rol import Rol
from excepciones.errores import CredencialesInvalidasError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio

MAX_INTENTOS_LOGIN = 3


def cargar_datos_iniciales(
    categoria_servicio: CategoriaServicio,
    producto_servicio: ProductoServicio,
    usuario_servicio: UsuarioServicio,
) -> None:
    usuario_servicio.crear("Ana", "Pérez", "admin@foodstore.com", "", "admin123", Rol.ADMIN)
    usuario_servicio.crear("Juan", "Gómez", "cliente@foodstore.com", "", "cliente123", Rol.USUARIO)

    bebidas = categoria_servicio.crear("Bebidas", "Gaseosas, jugos y aguas")
    comidas = categoria_servicio.crear("Comidas", "Platos principales")

    producto_servicio.crear("Coca-Cola 500ml", 1500.0, "Gaseosa", 20, "", True, bebidas)
    producto_servicio.crear("Hamburguesa clásica", 5200.0, "Con papas", 10, "", True, comidas)


def iniciar_sesion(usuario_servicio: UsuarioServicio):
    for intento in range(1, MAX_INTENTOS_LOGIN + 1):
        print("=== FOOD STORE – INICIO DE SESIÓN ===")
        mail = leer_texto("Mail: ")
        contrasenia = leer_texto("Contraseña: ")
        try:
            usuario = usuario_servicio.autenticar(mail, contrasenia)
            print(f"\nBienvenido/a, {usuario.nombre} {usuario.apellido} [{usuario.rol.value}]")
            return usuario
        except CredencialesInvalidasError as error:
            intentos_restantes = MAX_INTENTOS_LOGIN - intento
            if intentos_restantes > 0:
                print(f"{error}. Intentos restantes: {intentos_restantes}\n")
            else:
                print(f"{error}.")
    return None


def main() -> None:
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio()
    usuario_servicio = UsuarioServicio()
    pedido_servicio = PedidoServicio(producto_servicio)

    cargar_datos_iniciales(categoria_servicio, producto_servicio, usuario_servicio)

    while True:
        usuario = iniciar_sesion(usuario_servicio)
        if usuario is None:
            print("Se agotaron los intentos de inicio de sesión. Cerrando Food Store.")
            break

        menu = crear_menu(
            usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio
        )
        continuar_sesion = menu.mostrar()
        if not continuar_sesion:
            print("¡Gracias por usar Food Store!")
            break


if __name__ == "__main__":
    main()
