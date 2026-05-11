"""
Schemas Pydantic — Vehículos
Relación: tipo_vehiculo + empleados (conductor)
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date

from app.schemas.tipos_vehiculos import TipoVehiculoResponse
from app.schemas.empleados import EmpleadoResponse


class VehiculoBase(BaseModel):
    placa: str = Field(..., min_length=1, max_length=20, description="Placa del vehículo")
    id_tipo_vehiculo: int
    id_conductor: int = Field(..., description="ID del empleado conductor")
    anio_fabricacion: int = Field(..., ge=1900, le=2100)
    fecha_compra: Optional[date] = None
    estado: str = Field(default="activo", description="activo, inactivo, mantenimiento")


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=1, max_length=20)
    id_tipo_vehiculo: Optional[int] = None
    id_conductor: Optional[int] = None
    anio_fabricacion: Optional[int] = Field(None, ge=1900, le=2100)
    fecha_compra: Optional[date] = None
    estado: Optional[str] = None


class VehiculoResponse(VehiculoBase):
    model_config = ConfigDict(from_attributes=True)
    id_vehiculo: int


class VehiculoConRelaciones(VehiculoResponse):
    """Vehículo con datos del tipo y conductor."""
    tipo_vehiculo: Optional[TipoVehiculoResponse] = None
    conductor: Optional[EmpleadoResponse] = None


class VehiculoListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[VehiculoResponse]