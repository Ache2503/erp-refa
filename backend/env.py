from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Importar Base y TODOS los modelos para que Alembic los detecte ──
from app.core.database import Base

from app.models.backups import Backups
from app.models.categoria_padre import CategoriaPadre
from app.models.clientes import Clientes
from app.models.configuracion import Configuracion
from app.models.empleados import Empleados
from app.models.marcas import Marcas
from app.models.permisos import Permisos
from app.models.proveedores import Proveedores
from app.models.restauraciones import Restauraciones
from app.models.roles import Roles
from app.models.ruta import Ruta
from app.models.tipo_vehiculo import TipoVehiculo
from app.models.tipos_almacen import TiposAlmacen
from app.models.unidades_medida import UnidadesMedida
from app.models.almacenes import Almacenes
from app.models.auditoria import Auditoria
from backend.app.models.categorias import Categorias
from app.models.empleado_rol import EmpleadoRol
from app.models.movimiento import Movimiento
from app.models.proveedor_contacto import ProveedorContacto
from app.models.rol_permiso import RolPermiso
from app.models.vehiculo import Vehiculo
from app.models.compras import Compras
from app.models.mantenimiento_vehiculo import MantenimientoVehiculo
from app.models.pedidos_clientes import PedidosClientes
from app.models.pedidos_proveedores import PedidosProveedores
from app.models.productos import Productos
from app.models.traslados_internos import TrasladosInternos
from app.models.compra_detalle import CompraDetalle
from app.models.devoluciones_clientes import DevolucionesClientes
from app.models.devoluciones_proveedores import DevolucionesProveedores
from app.models.envios import Envios
from app.models.guia_remision import GuiaRemision
from app.models.movimiento_detalle import MovimientoDetalle
from app.models.pedido_cliente_detalle import PedidoClienteDetalle
from app.models.pedido_proveedor_detalle import PedidoProveedorDetalle
from app.models.productos_almacen import ProductosAlmacen
from app.models.traslado_interno_detalle import TrasladoInternoDetalle
from app.models.asignacion_transporte import AsignacionTransporte
from app.models.devolucion_cliente_detalle import DevolucionClienteDetalle
from app.models.devolucion_proveedor_detalle import DevolucionProveedorDetalle
from app.models.envio_detalle import EnvioDetalle
from app.models.guia_remision_detalle import GuiaRemisionDetalle
from app.models.ruta_envio import RutaEnvio
from app.models.seguimiento_envio import SeguimientoEnvio

# Metadata real con todos los modelos registrados
target_metadata = Base.metadata

# ── Configuración Alembic ────────────────────────────────────────
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Leer URL de BD desde variables de entorno (no desde alembic.ini)
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "erp_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "erp_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "gestion")

config.set_main_option(
    "sqlalchemy.url",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def run_migrations_offline() -> None:
    """Modo offline: genera SQL sin conectarse a la BD."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Modo online: se conecta a la BD y aplica migraciones."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()