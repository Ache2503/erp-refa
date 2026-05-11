"""
Schemas Pydantic — Tipos de Almacén
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TipoAlmacenBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = None


class TipoAlmacenCreate(TipoAlmacenBase):
    pass


class TipoAlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = None


class TipoAlmacenResponse(TipoAlmacenBase):
    model_config = ConfigDict(from_attributes=True)
    id_tipo_almacen: int


class TipoAlmacenListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[TipoAlmacenResponse]