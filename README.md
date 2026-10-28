# Food Store – Sistema de Gestión de Pedidos de Comida

Trabajo Práctico Integrador – Programación II – Tecnicatura Universitaria en Programación (UTN, a distancia).

## Integrantes

- Roberto Jaimes ([jaimesroberttto@gmail.com](mailto:jaimesroberttto@gmail.com))
- Gabriel Vega

## Cómo ejecutar

Requiere **Python 3.12 o superior**. Solo usa biblioteca estándar (no hace falta instalar dependencias).

```bash
cd food_store
python main.py
```

Para correr las pruebas del modelo y los servicios (sin menú interactivo):

```bash
cd food_store
python pruebas.py
```

> En Windows, si las tildes se ven mal en la consola (CMD/PowerShell), ejecutar antes `chcp 65001` o correr con `set PYTHONIOENCODING=utf-8` (es solo la codificación de la terminal, no afecta al programa).

## Credenciales del administrador inicial

| Mail                 | Contraseña |
|----------------------|------------|
| admin@foodstore.com  | admin123   |

También se carga un usuario cliente de ejemplo: `cliente@foodstore.com` / `cliente123`.

## Enlaces

- Video explicativo (10 a 15 minutos, con los dos integrantes a cámara al inicio): _(completar enlace)_
- Informe en PDF: _(completar enlace, o ver el PDF en la raíz del .zip entregado)_
- Repositorio GitHub: _(completar enlace)_

## Estructura del proyecto

```
food_store/
├── main.py            # crea los servicios y arranca el menú principal
├── pruebas.py          # pruebas del modelo y servicios, sin menú
├── entidades/          # clases del UML (Base, Categoria, Producto, Usuario, Pedido, DetallePedido)
│   └── calculable.py    # interfaz Calculable
├── enums/               # Rol, Estado, FormaPago
├── excepciones/         # FoodStoreError y sus subclases
├── servicios/            # un servicio por entidad (CategoriaServicio, ProductoServicio, ...)
└── consola/              # Menu, MenuAdministrador, MenuCliente y lectura validada
```

## Notas de diseño

- Todas las entidades heredan de `Base` (abstracta), que asigna el `id` con un contador de clase compartido y maneja la baja lógica (`eliminado`) y `creado_en`.
- `Pedido` implementa la interfaz `Calculable` y es el único que crea objetos `DetallePedido`.
- El menú se resuelve por polimorfismo (`MenuAdministrador` / `MenuCliente`), sin condicionales por rol repartidos en la consola.
- Toda la información vive en memoria: al cerrar el programa se pierde (comportamiento esperado).
