"""
Schemas Pydantic — Ventas
Venta directa (sin pedido previo)
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from decimal import Decimal


class VentaDetalleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente_detalle: int
    id_pedido_cliente: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal


# ── VENTA ──────────────────────────────────────────────────

class VentaBase(BaseModel):
    id_cliente: int
    id_empleado: int = Field(..., description="Vendedor")
    id_almacen: int = Field(default=1)


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    id_cliente: Optional[int] = None
    id_empleado: Optional[int] = None
    estatus: Optional[str] = None


class VentaResponse(VentaBase):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente: int
    fecha: date
    subtotal: Decimal
    impuesto: Decimal
    total: Decimal


class VentaConDetalles(VentaResponse):
    detalles: list[VentaDetalleResponse] = []
    id_pedido_cliente: int


class VentaListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[VentaResponse]