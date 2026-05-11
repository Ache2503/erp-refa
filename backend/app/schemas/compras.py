"""
Schemas Pydantic — Compras
Relaciones: proveedores + productos + almacenes + empleados
Tablas: compras + compra_detalle
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.schemas.proveedores import ProveedorResponse
from app.schemas.productos import ProductoResponse
from app.schemas.almacenes import AlmacenResponse
from app.schemas.empleados import EmpleadoResponse


class CompraDetalleBase(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2)
    descuento_porcentaje: Decimal = Field(default=0, ge=0, le=100, decimal_places=2)


class CompraDetalleCreate(CompraDetalleBase):
    pass


class CompraDetalleResponse(CompraDetalleBase):
    model_config = ConfigDict(from_attributes=True)
    id_compra_detalle: int
    subtotal: Decimal  # cantidad * precio_unitario
    descuento_monto: Decimal  # subtotal * (descuento_porcentaje / 100)
    total: Decimal  # subtotal - descuento_monto


class CompraDetalleConProducto(CompraDetalleResponse):
    producto: Optional[ProductoResponse] = None


# ── COMPRA (ORDEN) ────────────────────────────────────────────

class CompraBase(BaseModel):
    numero_orden: str = Field(..., min_length=1, max_length=50, description="Número único de orden")
    id_proveedor: int
    id_almacen: int = Field(..., description="Almacén de recepción")
    id_empleado: int = Field(..., description="Empleado responsable")
    fecha_pedido: datetime = Field(default_factory=datetime.now)
    fecha_entrega_esperada: Optional[datetime] = None
    estado: str = Field(default="pendiente", description="pendiente, confirmada, entregada, cancelada")
    notas: Optional[str] = None


class CompraCreate(CompraBase):
    detalles: list[CompraDetalleCreate] = Field(..., min_items=1)


class CompraUpdate(BaseModel):
    numero_orden: Optional[str] = Field(None, min_length=1, max_length=50)
    id_proveedor: Optional[int] = None
    id_almacen: Optional[int] = None
    id_empleado: Optional[int] = None
    fecha_entrega_esperada: Optional[datetime] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class CompraResponse(CompraBase):
    model_config = ConfigDict(from_attributes=True)
    id_compra: int
    total: Decimal  # suma de todos los detalles
    fecha_creacion: datetime


class CompraConDetalles(CompraResponse):
    """Compra con todos sus detalles."""
    detalles: list[CompraDetalleConProducto] = []


class CompraConRelaciones(CompraResponse):
    """Compra con relaciones."""
    proveedor: Optional[ProveedorResponse] = None
    almacen: Optional[AlmacenResponse] = None
    empleado: Optional[EmpleadoResponse] = None
    detalles: list[CompraDetalleConProducto] = []


class CompraListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[CompraResponse]