"""Genera el informe en PDF del TPI (Food Store) pedido por la consigna.

Arma: caratula, indice con numero de pagina, marco teorico, decisiones
tecnicas y arquitectura (con capturas de pantalla), dificultades y
soluciones, bibliografia/webgrafia y enlaces.

Las capturas se buscan por nombre de archivo dentro de informe/capturas/.
Si una captura todavia no existe, se dibuja un recuadro de reemplazo con
el nombre de archivo esperado y una descripcion de que mostrar, para que
el PDF se pueda generar (y entregar) incluso antes de sacarlas. Cuando se
agreguen las imagenes reales con esos mismos nombres, basta con volver a
correr este script para que el informe final las incluya.

Uso:
    python generar_informe.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fpdf import FPDF

CARPETA_INFORME = Path(__file__).resolve().parent
CARPETA_CAPTURAS = CARPETA_INFORME / "capturas"
ARCHIVO_SALIDA = CARPETA_INFORME.parent / "Informe_TPI_FoodStore.pdf"

INSTITUCION = "Tecnicatura Universitaria en Programación – UTN (a distancia)"
MATERIA = "Programación II"
TITULO_PROYECTO = "Food Store – Sistema de Gestión de Pedidos de Comida"
INTEGRANTES = ["Roberto Jaimes", "Gabriel Vega"]
FECHA_ENTREGA = "16/11/2026"

# Completar antes de armar el .zip final de entrega.
URL_REPOSITORIO = "https://github.com/jaimesroberttto/food_store"
URL_VIDEO = "[COMPLETAR: enlace al video de YouTube/Drive con permisos públicos]"

MARGEN = 20
ANCHO_UTIL = 210 - 2 * MARGEN


@dataclass(frozen=True)
class Captura:
    archivo: str
    descripcion: str


class InformePDF(FPDF):
    mostrar_pie: bool = False
    titulo_pie: str = ""

    def footer(self) -> None:
        if not self.mostrar_pie:
            return
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 10, f"{self.titulo_pie} - Página {self.page_no()}", align="C")


def nueva_pdf() -> InformePDF:
    pdf = InformePDF(orientation="P", unit="mm", format="A4")
    pdf.core_fonts_encoding = "cp1252"
    pdf.set_margins(MARGEN, MARGEN, MARGEN)
    pdf.set_auto_page_break(auto=True, margin=MARGEN)
    pdf.set_title(TITULO_PROYECTO)
    pdf.set_author(" / ".join(INTEGRANTES))
    return pdf


def titulo_seccion(pdf: FPDF, numero: str, texto: str) -> None:
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(20, 20, 20)
    encabezado = f"{numero}. {texto}" if numero else texto
    pdf.cell(0, 10, encabezado, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(180, 180, 180)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)


def subtitulo(pdf: FPDF, texto: str) -> None:
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def parrafo(pdf: FPDF, texto: str) -> None:
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(ANCHO_UTIL, 6, texto, new_x="LMARGIN")
    pdf.ln(1)


def lista(pdf: FPDF, items: list[str]) -> None:
    pdf.set_font("Helvetica", "", 11)
    for item in items:
        x_inicio = pdf.get_x()
        pdf.cell(5, 6, "-", new_x="END", new_y="TOP")
        pdf.set_x(x_inicio + 6)
        pdf.multi_cell(ANCHO_UTIL - 6, 6, item, new_x="LMARGIN")
    pdf.ln(1)


def placeholder_completar(pdf: FPDF, texto: str) -> None:
    pdf.set_font("Helvetica", "BI", 11)
    pdf.set_text_color(170, 90, 0)
    pdf.multi_cell(ANCHO_UTIL, 6, texto, new_x="LMARGIN")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def _tamano_imagen(pdf: FPDF, ruta: Path, ancho_max: float) -> tuple[float, float]:
    from PIL import Image

    with Image.open(ruta) as img:
        ancho_px, alto_px = img.size
    alto = ancho_max * alto_px / ancho_px
    alto_max = 95.0
    if alto > alto_max:
        alto = alto_max
        ancho_max = alto_max * ancho_px / alto_px
    return ancho_max, alto


def captura(pdf: FPDF, item: Captura) -> None:
    ruta = None
    for extension in (".png", ".jpg", ".jpeg"):
        candidata = CARPETA_CAPTURAS / f"{Path(item.archivo).stem}{extension}"
        if candidata.exists():
            ruta = candidata
            break

    if pdf.get_y() > 200:
        pdf.add_page()

    if ruta is not None:
        ancho, alto = _tamano_imagen(pdf, ruta, ANCHO_UTIL)
        x = pdf.l_margin + (ANCHO_UTIL - ancho) / 2
        pdf.image(str(ruta), x=x, y=pdf.get_y(), w=ancho, h=alto)
        pdf.set_draw_color(150, 150, 150)
        pdf.rect(x, pdf.get_y(), ancho, alto)
        pdf.set_y(pdf.get_y() + alto + 2)
    else:
        alto_caja = 55.0
        x = pdf.l_margin
        y = pdf.get_y()
        pdf.set_draw_color(200, 120, 0)
        pdf.set_dash_pattern(dash=2, gap=1.5)
        pdf.rect(x, y, ANCHO_UTIL, alto_caja)
        pdf.set_dash_pattern()
        pdf.set_xy(x + 4, y + 6)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(170, 90, 0)
        pdf.multi_cell(
            ANCHO_UTIL - 8, 5, f"CAPTURA PENDIENTE - archivo esperado: {item.archivo}", new_x="LMARGIN"
        )
        pdf.set_xy(x + 4, pdf.get_y() + 1)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(90, 90, 90)
        pdf.multi_cell(ANCHO_UTIL - 8, 5, f"Mostrar: {item.descripcion}", new_x="LMARGIN")
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(y + alto_caja + 2)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(ANCHO_UTIL, 5, item.descripcion, align="C", new_x="LMARGIN")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)


# ---------------------------------------------------------------------------
# Secciones
# ---------------------------------------------------------------------------


def portada(pdf: InformePDF) -> None:
    pdf.mostrar_pie = False
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("Helvetica", "B", 13)
    pdf.multi_cell(0, 7, INSTITUCION, align="C", new_x="LMARGIN")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7, "Trabajo Práctico Integrador", align="C", new_x="LMARGIN")
    pdf.multi_cell(0, 7, MATERIA, align="C", new_x="LMARGIN")

    pdf.ln(28)
    pdf.set_font("Helvetica", "B", 22)
    pdf.multi_cell(0, 11, TITULO_PROYECTO, align="C", new_x="LMARGIN")

    pdf.ln(28)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Integrantes:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    for integrante in INTEGRANTES:
        pdf.cell(0, 7, integrante, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(-45)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Fecha de entrega: {FECHA_ENTREGA}", align="C", new_x="LMARGIN", new_y="NEXT")


def indice(pdf: InformePDF, paginas: dict[str, int], offset: int) -> None:
    pdf.mostrar_pie = True
    pdf.titulo_pie = TITULO_PROYECTO
    pdf.add_page()
    titulo_seccion(pdf, "", "Índice")

    entradas = [
        ("1. Introducción y alcance del proyecto", paginas["introduccion"]),
        ("2. Marco teórico", paginas["marco_teorico"]),
        ("3. Decisiones técnicas y arquitectura", paginas["decisiones"]),
        ("4. Dificultades y soluciones", paginas["dificultades"]),
        ("5. Bibliografía y webgrafía", paginas["bibliografia"]),
        ("6. Enlaces", paginas["enlaces"]),
    ]

    pdf.set_font("Helvetica", "", 12)
    for texto, pagina_relativa in entradas:
        pagina = pagina_relativa + offset
        ancho_texto = pdf.get_string_width(texto)
        ancho_num = pdf.get_string_width(str(pagina))
        ancho_puntos = ANCHO_UTIL - ancho_texto - ancho_num - 2
        cantidad_puntos = max(3, int(ancho_puntos / pdf.get_string_width(".")))
        linea = f"{texto} {'.' * cantidad_puntos} {pagina}"
        pdf.cell(0, 9, linea, new_x="LMARGIN", new_y="NEXT")


def introduccion(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["introduccion"] = pdf.page_no()
    titulo_seccion(pdf, "1", "Introducción y alcance del proyecto")
    parrafo(
        pdf,
        "Food Store es un sistema de gestión de pedidos de comida desarrollado en Python "
        "aplicando el paradigma de Programación Orientada a Objetos (POO), como Trabajo "
        "Práctico Integrador de la materia Programación II. Permite administrar categorías, "
        "productos, usuarios y pedidos, con un inicio de sesión que distingue entre el rol "
        "ADMIN (gestión completa) y el rol USUARIO (solo consulta).",
    )
    parrafo(
        pdf,
        "Toda la información vive en memoria mientras el programa se ejecuta, organizada en "
        "colecciones dentro de los servicios de cada entidad; al cerrar el programa los datos "
        "se pierden, tal como establece la consigna. El proyecto respeta la arquitectura en "
        "tres capas pedida (entidades, servicios y consola), con validaciones de entrada y "
        "excepciones propias para que ningún dato mal ingresado cierre el programa.",
    )
    parrafo(
        pdf,
        "Como plus por fuera de lo pedido en la consigna, se agregó además una interfaz "
        "gráfica (Tkinter) que reutiliza exactamente los mismos servicios que la consola, sin "
        "duplicar reglas de negocio. El modo de consola original pedido por la consigna se "
        "conserva intacto y se ejecuta con el argumento --consola (ver sección de enlaces).",
    )


def marco_teorico(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["marco_teorico"] = pdf.page_no()
    titulo_seccion(pdf, "2", "Marco teórico")

    parrafo(
        pdf,
        "Python es un lenguaje de programación interpretado, multiparadigma y de tipado "
        "dinámico, ampliamente usado en la industria y la academia por su sintaxis simple y "
        "su extensa biblioteca estándar. Desde la versión 3.5 (PEP 484) incorpora soporte "
        "opcional para type hints: anotaciones de tipo en variables, parámetros y valores de "
        "retorno que no son verificadas en tiempo de ejecución, pero sí permiten que editores "
        "y herramientas de análisis estático (como mypy) detecten errores antes de correr el "
        "programa, y documentan el contrato de cada función o método. En este proyecto se "
        "utilizan en todos los atributos, parámetros y retornos, como pide la consigna.",
    )

    subtitulo(pdf, "Clase abstracta")
    parrafo(
        pdf,
        "Una clase abstracta define un contrato común para sus subclases sin poder ser "
        "instanciada directamente. En Python se implementa heredando de ABC (módulo abc) y "
        "marcando métodos con @abstractmethod. En Food Store, Base es la clase abstracta de la "
        "que heredan todas las entidades (Categoria, Producto, Usuario, Pedido y "
        "DetallePedido): centraliza el id autogenerado, la baja lógica (eliminado) y la fecha "
        "de alta (creado_en), y obliga a cada subclase a implementar __str__.",
    )

    subtitulo(pdf, "Interfaz")
    parrafo(
        pdf,
        "Una interfaz estandariza un comportamiento sin imponer una jerarquía de herencia de "
        "estado. Se modeló con la clase Calculable (también basada en ABC), que define un único "
        "método abstracto calcular_total() -> None. Pedido es la única clase que la implementa: "
        "recalcula su total a partir de los subtotales de sus detalles cada vez que se agrega o "
        "elimina un producto del pedido.",
    )

    subtitulo(pdf, "Herencia y polimorfismo")
    parrafo(
        pdf,
        "La herencia permite que Categoria, Producto, Usuario, Pedido y DetallePedido "
        "reutilicen el comportamiento común de Base sin repetirlo. El polimorfismo se usa para "
        "resolver el menú según el rol del usuario: Menu es una clase abstracta con el método "
        "mostrar(), y MenuAdministrador / MenuCliente son subclases concretas. El programa "
        "principal solo conoce la referencia a Menu y llama a menu.mostrar() sin ningún if "
        "repartido por rol; la decisión de qué subclase instanciar se toma en un único lugar "
        "(la función crear_menu).",
    )

    subtitulo(pdf, "Encapsulamiento")
    parrafo(
        pdf,
        "Todos los atributos de las entidades son privados (doble guion bajo) y se exponen "
        "mediante @property, con @<atributo>.setter en los que el sistema permite modificar; "
        "cada setter valida el dato antes de aceptarlo (por ejemplo, Producto.precio rechaza "
        "valores negativos lanzando PrecioInvalidoError). La contraseña de Usuario es la "
        "excepción explícita que pide la consigna: no tiene property de lectura, solo el método "
        "verificar_contrasenia(...), de modo que nunca sale del objeto.",
    )

    subtitulo(pdf, "Composición y agregación")
    parrafo(
        pdf,
        "Pedido compone sus DetallePedido: los crea él mismo a través de agregar_detalle(...) "
        "y son los únicos responsables de darlos de baja; un detalle no tiene sentido ni ciclo "
        "de vida fuera de su pedido. En cambio, la relación entre Categoria y Producto es de "
        "agregación: un producto referencia a su categoría, pero esta existe de forma "
        "independiente y puede seguir existiendo (o eliminarse, si no tiene productos activos) "
        "sin depender del ciclo de vida de un producto puntual.",
    )

    subtitulo(pdf, "Excepciones propias")
    parrafo(
        pdf,
        "Se definió una jerarquía de excepciones propias que heredan de FoodStoreError "
        "(EntidadNoEncontradaError, DatoInvalidoError y su subclase PrecioInvalidoError, "
        "StockInsuficienteError, DuplicadoError, OperacionNoPermitidaError y "
        "CredencialesInvalidasError). La consola captura FoodStoreError para mostrar mensajes "
        "de negocio claros, y ValueError para los errores de conversión de int()/float(), de "
        "forma que ningún dato mal ingresado cierra el programa.",
    )

    subtitulo(pdf, "Colecciones")
    parrafo(
        pdf,
        "Cada servicio (CategoriaServicio, ProductoServicio, UsuarioServicio, PedidoServicio) "
        "mantiene su propia colección en memoria (una lista privada) y es responsable de "
        "buscar, validar y aplicar las reglas de negocio que involucran a varios objetos de su "
        "entidad, como la unicidad del mail o del nombre de categoría.",
    )


def decisiones_tecnicas(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["decisiones"] = pdf.page_no()
    titulo_seccion(pdf, "3", "Decisiones técnicas y arquitectura")

    parrafo(
        pdf,
        "El proyecto se organiza en tres paquetes con dependencia en un solo sentido "
        "(consola -> servicios -> entidades), más enums/ y excepciones/ como paquetes "
        "transversales:",
    )
    lista(
        pdf,
        [
            "entidades/: clases del UML (Base, Categoria, Producto, Usuario, Pedido, "
            "DetallePedido) y la interfaz Calculable. No usan input() ni print(): solo "
            "guardan y validan su propio estado.",
            "servicios/: un servicio por entidad, con la colección en memoria y las reglas "
            "de negocio que cruzan varios objetos. No leen del teclado ni imprimen.",
            "consola/: Menu (abstracta), MenuAdministrador, MenuCliente, la fábrica "
            "crear_menu(...) y los helpers de lectura validada (consola/lectura.py). Es la "
            "única capa que conoce input()/print() y captura las excepciones de negocio.",
            "gui/: interfaz gráfica Tkinter agregada como plus. Llama a los mismos "
            "servicios que la consola; no contiene reglas de negocio propias.",
            "main.py: crea los servicios, carga los datos iniciales y arranca el modo "
            "consola o gráfico según el argumento --consola. No contiene reglas de negocio.",
        ],
    )

    subtitulo(pdf, "El id y la baja lógica")
    parrafo(
        pdf,
        "Base asigna el id automáticamente con un contador de clase compartido por todas las "
        "entidades (Base._contador_id), de forma que cada objeto del sistema tiene un "
        "identificador único sin importar su tipo. Toda baja es lógica: se marca eliminado = "
        "True y el objeto permanece en la colección para no perder el historial (por ejemplo, "
        "los pedidos de un usuario eliminado se siguen pudiendo consultar).",
    )

    subtitulo(pdf, "Pedido como único creador de sus detalles")
    parrafo(
        pdf,
        "Pedido es la única clase que instancia DetallePedido, a través de "
        "agregar_detalle(cantidad, producto). El subtotal de cada detalle se calcula con el "
        "precio del producto en el momento de agregarlo (no con un valor que escriba el "
        "operador), y si el producto ya tenía un detalle en el pedido, se suma la cantidad en "
        "lugar de crear uno nuevo. La propiedad detalles devuelve una tupla (copia inmutable), "
        "para que nadie pueda modificar la lista interna desde afuera del pedido.",
    )

    subtitulo(pdf, "Transiciones de estado")
    parrafo(
        pdf,
        "Las transiciones válidas (PENDIENTE -> CONFIRMADO -> TERMINADO; PENDIENTE o "
        "CONFIRMADO -> CANCELADO) se modelan con un diccionario de conjuntos "
        "(_TRANSICIONES_VALIDAS) dentro de Pedido.cambiar_estado(...), que lanza "
        "OperacionNoPermitidaError ante cualquier cambio no contemplado. Al cancelar o eliminar "
        "un pedido que no llegó a TERMINADO, PedidoServicio devuelve el stock reservado de cada "
        "producto.",
    )

    subtitulo(pdf, "Pantallas del sistema en funcionamiento")
    parrafo(
        pdf,
        "A continuación se incluyen capturas del sistema recorriendo el flujo principal: "
        "inicio de sesión con ambos roles, alta y listados desde el menú de administrador, un "
        "error de validación y un pedido cancelado por falta de stock.",
    )

    for item in CAPTURAS_REQUERIDAS:
        captura(pdf, item)


def dificultades(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["dificultades"] = pdf.page_no()
    titulo_seccion(pdf, "4", "Dificultades y soluciones")

    subtitulo(pdf, "Dificultades técnicas propias del diseño (ya resueltas en el código)")
    lista(
        pdf,
        [
            "No exponer la contraseña del usuario ni la lista interna de detalles de un "
            "pedido: se resolvió sin property de lectura para la contraseña (solo "
            "verificar_contrasenia) y devolviendo una tupla inmutable desde Pedido.detalles.",
            "Evitar condicionales por rol repartidos en la consola: se resolvió modelando "
            "Menu como clase abstracta con una subclase por rol, decidiendo cuál instanciar "
            "en un único punto (crear_menu).",
            "Que el total de un pedido nunca quede desincronizado de sus detalles: se "
            "resolvió recalculándolo con calcular_total() dentro de la propia clase Pedido "
            "cada vez que se agrega o elimina un detalle, en lugar de dejarlo a cargo de la "
            "consola.",
            "Mantener la consistencia del stock ante cancelaciones y bajas: se resolvió "
            "centralizando el descuento y la devolución de stock en PedidoServicio, que se "
            "invoca siempre desde los mismos dos puntos (cambiar_estado y eliminar).",
        ],
    )

    placeholder_completar(
        pdf,
        "[COMPLETAR EN EQUIPO: agregar 2 o 3 dificultades propias del proceso de trabajo "
        "(por ejemplo, coordinación entre los dos integrantes, dudas puntuales con "
        "type hints, organización del repositorio, pruebas manuales de la GUI, etc.) y cómo "
        "las resolvieron. Reemplazar este párrafo antes de la entrega final.]",
    )


def bibliografia(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["bibliografia"] = pdf.page_no()
    titulo_seccion(pdf, "5", "Bibliografía y webgrafía")

    lista(
        pdf,
        [
            "Python Software Foundation. Documentación oficial de Python 3 - "
            "https://docs.python.org/es/3/",
            "Python Software Foundation. Módulo abc - Abstract Base Classes - "
            "https://docs.python.org/es/3/library/abc.html",
            "Python Software Foundation. Módulo enum - "
            "https://docs.python.org/es/3/library/enum.html",
            "Python Software Foundation. Módulo datetime - "
            "https://docs.python.org/es/3/library/datetime.html",
            "Python Software Foundation. Módulo typing y type hints - "
            "https://docs.python.org/es/3/library/typing.html",
            "PEP 484 - Type Hints - https://peps.python.org/pep-0484/",
            "Python Software Foundation. Documentación de tkinter - "
            "https://docs.python.org/es/3/library/tkinter.html",
            "[COMPLETAR: agregar aquí cualquier otro recurso, video o apunte de cátedra "
            "que hayan consultado durante el desarrollo.]",
        ],
    )


def enlaces(pdf: InformePDF, paginas: dict[str, int]) -> None:
    pdf.add_page()
    paginas["enlaces"] = pdf.page_no()
    titulo_seccion(pdf, "6", "Enlaces")

    subtitulo(pdf, "Repositorio GitHub")
    parrafo(pdf, URL_REPOSITORIO)

    subtitulo(pdf, "Video explicativo (10 a 15 minutos)")
    parrafo(pdf, URL_VIDEO)

    subtitulo(pdf, "Cómo ejecutar el proyecto")
    lista(
        pdf,
        [
            "Modo consola (el pedido por la consigna): python main.py --consola",
            "Modo gráfico (plus agregado, Tkinter): python main.py",
            "Pruebas del modelo y los servicios, sin menú: python pruebas.py",
        ],
    )


CAPTURAS_REQUERIDAS = [
    Captura(
        "login_admin.png",
        "Pantalla de inicio de sesión mostrando el ingreso exitoso como ADMIN "
        "(saludo con nombre y rol).",
    ),
    Captura(
        "menu_admin.png",
        "Menú principal del administrador, con las cuatro secciones de gestión.",
    ),
    Captura(
        "crear_producto.png",
        "Alta de un producto nuevo desde el submenú de Productos, con el id generado.",
    ),
    Captura(
        "error_validacion.png",
        "Un error de validación de negocio en consola o en la GUI (por ejemplo, precio "
        "negativo, mail duplicado o nombre de categoría repetido) mostrando el mensaje "
        "de error sin cerrar el programa.",
    ),
    Captura(
        "pedido_cancelado_stock.png",
        "Un pedido cancelado por falta de stock: el intento de agregar una cantidad "
        "mayor al stock disponible, rechazado con StockInsuficienteError.",
    ),
    Captura(
        "login_cliente.png",
        "Inicio de sesión exitoso como USUARIO (cliente) y su menú de solo consulta.",
    ),
    Captura(
        "mis_pedidos_cliente.png",
        "El cliente consultando 'Mis pedidos' y el detalle de uno de ellos.",
    ),
]


def generar() -> None:
    CARPETA_CAPTURAS.mkdir(exist_ok=True)

    pdf_medicion = nueva_pdf()
    paginas: dict[str, int] = {}
    introduccion(pdf_medicion, paginas)
    marco_teorico(pdf_medicion, paginas)
    decisiones_tecnicas(pdf_medicion, paginas)
    dificultades(pdf_medicion, paginas)
    bibliografia(pdf_medicion, paginas)
    enlaces(pdf_medicion, paginas)

    pdf_final = nueva_pdf()
    portada(pdf_final)
    indice(pdf_final, paginas, offset=2)
    introduccion(pdf_final, {})
    marco_teorico(pdf_final, {})
    decisiones_tecnicas(pdf_final, {})
    dificultades(pdf_final, {})
    bibliografia(pdf_final, {})
    enlaces(pdf_final, {})

    pdf_final.output(str(ARCHIVO_SALIDA))
    print(f"Informe generado en: {ARCHIVO_SALIDA}")

    faltantes = [
        item.archivo
        for item in CAPTURAS_REQUERIDAS
        if not any(
            (CARPETA_CAPTURAS / f"{Path(item.archivo).stem}{ext}").exists()
            for ext in (".png", ".jpg", ".jpeg")
        )
    ]
    if faltantes:
        print("\nCapturas todavía pendientes (se incluyó un recuadro de reemplazo):")
        for nombre in faltantes:
            print(f"  - {CARPETA_CAPTURAS / nombre}")


if __name__ == "__main__":
    generar()
