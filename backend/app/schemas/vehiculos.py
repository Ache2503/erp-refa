from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class VehiculoBase(BaseModel):
    placa: str = Field(..., min_length=1, max_length=20)
    marca: str = Field(..., min_length=1, max_length=50)
    id_tipo_vehiculo: int
    modelo: Optional[str] = None
    anio: Optional[int] = None
    numero_serie: Optional[str] = None
    capacidad_carga: Optional[Decimal] = None


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=1, max_length=20)
    marca: Optional[str] = Field(None, min_length=1, max_length=50)
    id_tipo_vehiculo: Optional[int] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    numero_serie: Optional[str] = None
    capacidad_carga: Optional[Decimal] = None


class VehiculoResponse(VehiculoBase):
    model_config = ConfigDict(from_attributes=True)
    id_vehiculo: int


class VehiculoListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[VehiculoResponse]
