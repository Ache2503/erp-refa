"""
Schemas Pydantic — Marcas
Simple CRUD sin dependencias complejas.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MarcaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class MarcaCreate(MarcaBase):
    pass


class MarcaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None


class MarcaResponse(MarcaBase):
    model_config = ConfigDict(from_attributes=True)
    id_marca: int


class MarcaListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[MarcaResponse]