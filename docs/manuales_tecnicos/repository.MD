📖 Manual Técnico: Controladores de Productos
Archivo: proyecto-erp/backend/app/api/productos/controllers.py

1. Propósito General del Archivo
Este archivo actúa como el "Recepcionista" de la API para todo lo relacionado con los productos. Su única responsabilidad es recibir las peticiones HTTP (las llamadas que hace el navegador o la aplicación frontend), delegar el trabajo pesado al servicio (ProductoService), y devolver la respuesta formateada al cliente.

No contiene lógica de negocio (no toma decisiones) ni se conecta directamente a la base de datos; solo enruta el tráfico.

2. Desglose de Importaciones Clave
Antes de las rutas, el archivo importa herramientas esenciales:

APIRouter: Es una clase de FastAPI que nos permite agrupar todas las rutas relacionadas con "Productos" en un solo lugar, en lugar de tener todo amontonado en el archivo principal (main.py).

Depends(get_db): Es el sistema de Inyección de Dependencias de FastAPI. Se asegura de que cada vez que alguien haga una petición, se abra una conexión (sesión) a la base de datos de forma segura y se cierre al terminar.

ProductoService: La clase que contiene la "inteligencia" y las reglas de negocio.

Esquemas (ProductoCreate, ProductoResponse, etc.): Los "moldes" que validan que la información que entra y sale tenga el formato correcto.

3. Configuración del Enrutador
Python
router = APIRouter(prefix="/productos", tags=["Productos"])
Esta línea es fundamental. Define que todas las rutas dentro de este archivo comenzarán automáticamente con /productos. Además, la etiqueta tags=["Productos"] agrupa estos endpoints de forma visual y ordenada en la documentación interactiva (Swagger UI) que genera FastAPI.

4. Análisis de los Endpoints (Rutas)
🟢 Crear un Producto (POST)
Python
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.crear_producto(producto)
¿Qué hace?: Recibe los datos de un producto nuevo y lo guarda en el sistema.

Entrada: Espera un objeto JSON que cumpla con las reglas de ProductoCreate (nombre, precio, código, etc.).

Respuesta: Devuelve el producto recién creado (con su nuevo id_producto asignado) y un código de estado 201 Created que indica éxito rotundo.

🔵 Obtener un Solo Producto (GET)
Python
@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.obtener_producto(producto_id)
¿Qué hace?: Busca los detalles de un producto específico utilizando su ID.

Entrada: El producto_id viaja directamente en la URL (ej. /productos/15). FastAPI valida automáticamente que este valor sea un número entero (int).

Respuesta: Devuelve los datos del producto usando el formato ProductoResponse.

🔵 Listar Múltiples Productos (GET)
Python
@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = ProductoService(db)
    return service.listar_productos(skip, limit)
¿Qué hace?: Devuelve un catálogo de productos. Implementa paginación para no colapsar la base de datos si hay miles de registros.

Entrada: Recibe dos parámetros opcionales en la URL (ej. /productos/?skip=0&limit=50).

skip: Cuántos registros saltarse (útil para la página 2, página 3, etc.).

limit: Cuántos registros traer máximo (restringido a un tope de 1000 por seguridad).

Respuesta: Una lista (List) de objetos ProductoResponse.

🟡 Actualizar un Producto (PUT)
Python
@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.actualizar_producto(producto_id, producto)
¿Qué hace?: Modifica la información de un producto existente.

Entrada: Necesita dos cosas. El producto_id en la URL para saber cuál producto actualizar, y un JSON (ProductoUpdate) en el cuerpo de la petición con los nuevos datos.

Respuesta: Devuelve el producto ya actualizado.

🔴 Eliminar un Producto (DELETE)
Python
@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ProductoService(db)
    service.eliminar_producto(producto_id)
    return None
¿Qué hace?: Borra un producto del sistema basándose en su ID.

Respuesta: Utiliza el código de estado 204 No Content. Esto significa que la operación fue un éxito, pero no hay datos adicionales que devolver en la respuesta (por eso retorna None).