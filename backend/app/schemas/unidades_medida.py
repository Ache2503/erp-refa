"""
Schemas Pydantic — Unidades de Medida
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UnidadMedidaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    abreviatura: str = Field(..., min_length=1, max_length=10)


class UnidadMedidaCreate(UnidadMedidaBase):
    pass


class UnidadMedidaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    abreviatura: Optional[str] = Field(None, min_length=1, max_length=10)


class UnidadMedidaResponse(UnidadMedidaBase):
    model_config = ConfigDict(from_attributes=True)
    id_unidad_medida: int


class UnidadMedidaListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[UnidadMedidaResponse]