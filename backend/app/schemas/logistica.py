"""
Schemas Pydantic — Logística / Envíos
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class EnvioDetalleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_detalle: int
    id_envio: int
    id_producto: int
    cantidad: int


# ── ENVÍO ──────────────────────────────────────────────────

class EnvioBase(BaseModel):
    id_pedido_cliente: int
    id_vehiculo: int
    id_empleado: int
    estatus: str = Field(default="pendiente")


class EnvioCreate(EnvioBase):
    pass


class EnvioUpdate(BaseModel):
    id_vehiculo: Optional[int] = None
    id_empleado: Optional[int] = None
    estatus: Optional[str] = None


class EnvioResponse(EnvioBase):
    model_config = ConfigDict(from_attributes=True)
    id_envio: int
    id_pedido_cliente: int


class EnvioConDetalles(EnvioResponse):
    detalles: list[EnvioDetalleResponse] = []


class EnvioListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[EnvioResponse]


# ── RUTA DE ENVÍO ─────────────────────────────────────────────

class RutaEnvioBase(BaseModel):
    orden: int = Field(..., ge=1)
    direccion: str = Field(..., min_length=1)
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None


class RutaEnvioCreate(RutaEnvioBase):
    pass


class RutaEnvioResponse(RutaEnvioBase):
    model_config = ConfigDict(from_attributes=True)
    id_ruta: int
    id_envio: int