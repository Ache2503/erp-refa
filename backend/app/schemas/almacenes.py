"""
Schemas Pydantic — Almacenes
Relación: empleados + tipos_almacen
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.schemas.empleados import EmpleadoResponse
from app.schemas.tipos_almacen import TipoAlmacenResponse


class AlmacenBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    ubicacion: Optional[str] = Field(None, max_length=200)
    id_empleado: int = Field(..., description="ID del empleado responsable")
    id_tipo_almacen: int = Field(..., description="Tipo de almacén")


class AlmacenCreate(AlmacenBase):
    pass


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    ubicacion: Optional[str] = Field(None, max_length=200)
    id_empleado: Optional[int] = None
    id_tipo_almacen: Optional[int] = None


class AlmacenResponse(AlmacenBase):
    model_config = ConfigDict(from_attributes=True)
    id_almacen: int


class AlmacenConRelaciones(AlmacenResponse):
    """Almacén con datos del empleado y tipo."""
    empleado: Optional[EmpleadoResponse] = None
    tipo_almacen: Optional[TipoAlmacenResponse] = None


class AlmacenListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[AlmacenResponse]