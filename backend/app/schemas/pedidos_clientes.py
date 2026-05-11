"""
Schemas Pydantic — Pedidos Clientes
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class PedidoClienteDetalleBase(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., gt=0)


class PedidoClienteDetalleCreate(PedidoClienteDetalleBase):
    pass


class PedidoClienteDetalleResponse(PedidoClienteDetalleBase):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente_detalle: int
    id_pedido_cliente: int
    subtotal: Decimal


# ── PEDIDO CLIENTE (ORDEN DE VENTA) ─────────────────────────

class PedidoClienteBase(BaseModel):
    id_cliente: int
    id_empleado: int
    id_almacen: int = Field(default=1)
    estatus: str = Field(default="pendiente")


class PedidoClienteCreate(PedidoClienteBase):
    pass


class PedidoClienteUpdate(BaseModel):
    id_cliente: Optional[int] = None
    id_empleado: Optional[int] = None
    id_almacen: Optional[int] = None
    estatus: Optional[str] = None


class PedidoClienteResponse(PedidoClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente: int
    fecha: date
    subtotal: Decimal
    impuesto: Decimal
    total: Decimal


class PedidoClienteConDetalles(PedidoClienteResponse):
    """Pedido con todos sus detalles."""
    detalles: list[PedidoClienteDetalleResponse] = []


class PedidoClienteListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[PedidoClienteResponse]