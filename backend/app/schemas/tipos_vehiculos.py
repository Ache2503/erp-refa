"""
Schemas Pydantic — Tipos de Vehículos
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TipoVehiculoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    capacidad_ton: Optional[float] = Field(None, gt=0, description="Capacidad en toneladas")
    descripcion: Optional[str] = None


class TipoVehiculoCreate(TipoVehiculoBase):
    pass


class TipoVehiculoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    capacidad_ton: Optional[float] = None
    descripcion: Optional[str] = None


class TipoVehiculoResponse(TipoVehiculoBase):
    model_config = ConfigDict(from_attributes=True)
    id_tipo_vehiculo: int


class TipoVehiculoListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[TipoVehiculoResponse]