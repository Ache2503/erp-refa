# Sistema ERP - API REST

Sistema de planificación de recursos empresariales con backend en FastAPI y base de datos MySQL.

## Tech Stack

- **Framework:** FastAPI 0.115.6
- **ORM:** SQLAlchemy 2.0.36
- **Base de datos:** MySQL (PyMySQL)
- **Auth:** Python-Jose + Passlib
- **Server:** Uvicorn

## Estructura del Proyecto

```
backend/
├── app/
│   ├── api/              # Controladores (endpoints)
│   ├── core/            # Configuración BD
│   ├── models/          # Modelos SQLAlchemy
│   ├── repositories/   # Acceso a datos
│   ├── schemas/        # Schemas Pydantic
│   ├── services/       # Lógica de negocio
│   └── utils/         # Utilidades
├── migrations/         # Alembic
└── run.py             # Entry point
```

## Endpoints Disponibles

| Módulo | Prefijo | Métodos |
|--------|--------|--------|
| Auth | `/auth` | POST (login, logout, register) |
| Roles & Permisos | `/roles`, `/permisos` | GET, POST, PUT, DELETE |
| Empleados | `/empleados` | GET, POST, PUT, DELETE, PATCH |
| Clientes | `/clientes` | GET, POST, PUT, DELETE, PATCH |
| Proveedores | `/proveedores` | GET, POST, PUT, DELETE |
| Categorías | `/categorias` | GET, POST, PUT, DELETE |
| Marcas | `/marcas` | GET, POST, PUT, DELETE |
| Unidades Medida | `/unidades-medida` | GET, POST, PUT, DELETE |
| Almacenes | `/almacenes` | GET, POST, PUT, DELETE |
| Tipos Almacén | `/tipos-almacen` | GET, POST, PUT, DELETE |
| Vehículos | `/vehiculos` | GET, POST, PUT, DELETE |
| Tipos Vehículos | `/tipos-vehiculos` | GET |
| Productos | `/productos` | GET, POST, PUT, DELETE |
| Compras | `/compras` | GET, POST, PUT, DELETE |
| Ventas | `/ventas` | GET, POST, PUT, DELETE |
| Logística | `/logistica` | GET, POST, PUT, DELETE |
| Pedidos Clientes | `/pedidos-clientes` | GET, POST, PUT, DELETE |

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux
# venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp env.example .env
# Editar .env con configuración de BD

# 4. Ejecutar migraciones (si aplica)
alembic upgrade head

# 5. Iniciar servidor
python run.py
```

## Configuración (.env)

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=erp_db
DB_USER=root
DB_PASSWORD=tu_password

APP_NAME=ERP API
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
```

## Documentación API

Una vez iniciado el servidor:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Ejemplos de Uso

### Crear Cliente
```bash
curl -X POST "http://localhost:8000/clientes" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com"}'
```

### Crear Producto (requiere categoría, marca y unidad existentes)
```bash
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell",
    "codigo": "LAP-001",
    "id_categoria": 1,
    "id_marca": 1,
    "id_unidad_medida": 1,
    "precio": 1500.00
  }'
```

### Listar Pedidos
```bash
curl -X GET "http://localhost:8000/pedidos-clientes"
```

## Estados de Entidades

| Entidad | Estados |
|--------|---------|
| Productos | activo, inactivo |
| Empleados | activo, inactivo |
| Clientes | activo, inactivo |
| Pedidos Clientes | pendiente, confirmado, despachado, entregado, cancelado |
| Compras | pendiente, confirmada, entregada, cancelada |
| Envíos | pendiente, en_transito, entregado |

## Licencia

MIT