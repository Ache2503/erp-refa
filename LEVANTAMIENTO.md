# Guía de Levantamiento — ERP Logístico

## 1. Requisitos del Sistema

| Herramienta | Versión Mínima |
|-------------|---------------|
| Python      | 3.12+         |
| Node.js     | 18+           |
| MySQL       | 8.0+          |
| Docker      | 24+ (opcional)|
| Docker Compose | 2.20+ (opcional) |

---

## 2. Estructura del Proyecto

```
erp-final/
├── backend/                    # API REST (FastAPI)
│   ├── app/
│   │   ├── api/              # Controladores (rutas/endpoints)
│   │   ├── core/             # Configuración y conexión BD
│   │   ├── models/           # Modelos SQLAlchemy (45 tablas)
│   │   ├── repositories/     # Capa de acceso a datos
│   │   ├── schemas/          # Esquemas Pydantic (validación)
│   │   ├── services/         # Lógica de negocio
│   │   ├── tasks/            # Tareas asíncronas (Celery)
│   │   └── utils/            # Utilidades
│   ├── migrations/           # Migraciones Alembic
│   ├── requirements.txt
│   └── run.py                # Entry point del servidor
├── frontend/                   # SPA (React + Vite + Tailwind)
│   ├── src/
│   │   ├── components/       # Componentes reutilizables
│   │   ├── pages/            # Páginas del sistema (16 módulos)
│   │   ├── context/          # AuthContext (estado de autenticación)
│   │   ├── hooks/            # useApi (cliente HTTP)
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── schema/               # Scripts SQL (esquema + datos iniciales)
├── docker-compose.yml         # MySQL + phpMyAdmin + Redis
└── docs/                      # Documentación técnica
```

---

## 3. Opción A: Levantamiento con Docker (recomendado)

### 3.1 Iniciar servicios de infraestructura

```bash
# Desde la raíz del proyecto
docker compose up -d
```

Esto levanta:
| Servicio    | Puerto | Descripción                     |
|-------------|--------|---------------------------------|
| MySQL       | 3307   | Base de datos (externa)         |
| phpMyAdmin  | 8080   | Administrador BD (user: root, pass: rootpass) |
| Redis       | 6379   | Cola de tareas (Celery)         |

### 3.2 Crear la base de datos y cargar schema

```bash
# Ejecutar script SQL
docker exec -i erp_mysql mysql -u root -prootpass gestion < database/schema/gestion_v2.sql

# Opcional: cargar datos de prueba
docker exec -i erp_mysql mysql -u root -prootpass gestion < database/schema/gestion_v2_insert.sql
```

---

## 4. Opción B: Levantamiento Manual

### 4.1 Base de datos MySQL

```bash
# Crear base de datos
mysql -u root -p
CREATE DATABASE gestion;
USE gestion;
SOURCE database/schema/gestion_v2.sql;
SOURCE database/schema/gestion_v2_insert.sql;   # datos de prueba
```

### 4.2 Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (ajustar según tu configuración)
cat > .env << 'EOF'
DB_HOST=localhost
DB_PORT=3306
DB_USER=erp_user
DB_PASSWORD=erp_pass
DB_NAME=gestion

APP_NAME="ERP API"
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

SECRET_KEY=your-secret-key-change-in-production
EOF

# Ejecutar migraciones (agrega columna password_hash)
alembic upgrade head

# Asignar contraseñas a empleados existentes
python seed_passwords.py

# Iniciar servidor
python run.py
```

El servidor se iniciará en `http://localhost:8000`.

### 4.3 Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar en modo desarrollo
npm run dev
```

El frontend se iniciará en `http://localhost:5173`.

---

## 5. Acceso al Sistema

| Recurso           | URL                            |
|-------------------|--------------------------------|
| Frontend (dev)    | http://localhost:5173          |
| API               | http://localhost:8000          |
| Swagger Docs      | http://localhost:8000/docs     |
| ReDoc             | http://localhost:8000/redoc    |
| Health Check      | http://localhost:8000/health   |
| phpMyAdmin        | http://localhost:8080          |

---

## 6. Módulos del Sistema

### Backend — Endpoints Disponibles

| Módulo               | Prefijo               | Métodos                          |
|----------------------|-----------------------|----------------------------------|
| Auth                 | `/auth`               | POST (login, logout, register)   |
| Roles & Permisos     | `/roles`, `/permisos` | GET, POST, PUT, DELETE           |
| Empleados            | `/empleados`          | GET, POST, PUT, DELETE, PATCH    |
| Clientes             | `/clientes`           | GET, POST, PUT, DELETE, PATCH    |
| Proveedores          | `/proveedores`        | GET, POST, PUT, DELETE           |
| Categorías           | `/categorias`         | GET, POST, PUT, DELETE           |
| Marcas               | `/marcas`             | GET, POST, PUT, DELETE           |
| Unidades Medida      | `/unidades-medida`    | GET, POST, PUT, DELETE           |
| Almacenes            | `/almacenes`          | GET, POST, PUT, DELETE           |
| Tipos Almacén        | `/tipos-almacen`      | GET, POST, PUT, DELETE           |
| Vehículos            | `/vehiculos`          | GET, POST, PUT, DELETE           |
| Tipos Vehículos      | `/tipos-vehiculos`    | GET, POST                         |
| Productos            | `/productos`          | GET, POST, PUT, DELETE           |
| Inventario           | `/inventario`         | GET, POST, PUT, DELETE, AJUSTAR  |
| Compras              | `/compras`            | GET, POST, PUT, DELETE           |
| Ventas               | `/ventas`             | GET, POST, PUT, DELETE           |
| Logística            | `/logistica`          | GET, POST, PUT, DELETE           |
| Pedidos Clientes     | `/pedidos-clientes`   | GET, POST, PUT, DELETE           |

### Frontend — Páginas (16 módulos)

- Dashboard, Empleados, Clientes, Proveedores
- Productos, Categorías, Marcas
- Inventario, Compras, Ventas, Pedidos
- Envíos, Traslados, Vehículos, Almacenes
- Roles y Permisos

---

## 7. Arquitectura del Backend (por capas)

```
[Cliente HTTP] → [API Router] → [Service] → [Repository] → [SQLAlchemy Model] → [MySQL]
                        ↕
                  [Pydantic Schema]
```

Cada capa tiene una responsabilidad específica:

| Capa          | Responsabilidad                                   |
|---------------|---------------------------------------------------|
| `api/`        | Rutas, validación de entrada, códigos HTTP        |
| `services/`   | Lógica de negocio, orquestación, reglas           |
| `repositories/` | Acceso a datos, consultas SQL (CRUD)           |
| `models/`     | Definición de tablas y relaciones (ORM)           |
| `schemas/`    | Validación de datos de entrada/salida (Pydantic)  |

---

## 8. Variables de Entorno

### Backend (`.env`)

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=erp_user
DB_PASSWORD=erp_pass
DB_NAME=gestion

# Aplicación
APP_NAME="ERP API"
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379/0
```

### Frontend (opcional, `.env`)

```env
VITE_API_URL=http://localhost:8000
```

---

## 9. Usuarios y Credenciales

Después de ejecutar la migración y el seed, los empleados existentes tienen contraseña:

| Email | Contraseña | Rol |
|-------|-----------|-----|
| `admin@erp.com` | `admin123` | Sin rol asignado |
| `juan@test.com` | `admin123` | Sin rol asignado |
| `maria@test.com` | `admin123` | Sin rol asignado |
| `carlos@test.com` | `admin123` | Sin rol asignado |
| `ana@test.com` | `admin123` | Sin rol asignado |
| `pedro@test.com` | `admin123` | Sin rol asignado |

> Puedes asignar roles desde el endpoint `POST /roles` o directamente en BD.

Para registrar un nuevo usuario, usa `POST /auth/register`:

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo@email.com",
    "password": "mi_password",
    "nombre": "Juan",
    "apellido": "Pérez",
    "cargo": "Vendedor"
  }'
```

---

## 10. Notas sobre el estado actual

| Aspecto                  | Estado                        |
|--------------------------|-------------------------------|
| Autenticación (login)    | ✅ Implementado (JWT + bcrypt)     |
| Dockerfile backend       | ⚠️ Vacío (usar `python run.py`)    |
| FormBuilder.jsx          | ⚠️ Vacío (no usado)               |
| init_db.py               | ⚠️ Vacío (usar scripts SQL)       |
| Archivos duplicados      | ⚠️ `venta`/`ventas`, `compra`/`compras`, `producto`/`productos` |
| Migraciones Alembic      | ✅ Configuradas, 3 versiones       |
| CRUD genérico frontend   | ✅ Funcional (CrudPage)           |
| Dashboard                | ✅ Conectado a API real           |
| 45 modelos BD            | ✅ Completos                      |

---

## 11. Comandos rápidos para migraciones

```bash
# Ver logs de MySQL
docker compose logs -f mysql

# Acceder a MySQL
docker exec -it erp_mysql mysql -u root -prootpass gestion

# Ver migraciones pendientes
cd backend && alembic current

# Generar nueva migración
cd backend && alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
cd backend && alembic upgrade head

# Asignar contraseñas a empleados existentes
cd backend && python seed_passwords.py

# Construir frontend para producción
cd frontend && npm run build
```

---

## 12. Resolución de problemas

| Problema                     | Posible solución                                        |
|------------------------------|---------------------------------------------------------|
| Puerto 3307 ocupado          | Cambiar en `docker-compose.yml` el mapeo de puertos     |
| Error de conexión MySQL      | Verificar credenciales en `.env` y docker-compose.yml   |
| CORS error                   | Backend ya permite `*`, verificar puerto del frontend   |
| `alembic upgrade head` falla | Asegurar que `DB_HOST` apunte a `localhost`             |
| Frontend no conecta          | Verificar `VITE_API_URL` o que el backend esté corriendo |
