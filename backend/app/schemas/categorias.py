"""
Schemas Pydantic — Categorías
Soporta jerarquía: categoria_padre → categorias
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CategoriaPadreBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)


class CategoriaPadreCreate(CategoriaPadreBase):
    pass


class CategoriaPadreUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)


class CategoriaPadreResponse(CategoriaPadreBase):
    model_config = ConfigDict(from_attributes=True)
    id_categoria_padre: int


# ── Categoría (subcategoría) ──────────────────────────────────────

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    id_categoria_padre: Optional[int] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    id_categoria_padre: Optional[int] = None


class CategoriaResponse(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)
    id_categoria: int


class CategoriaConPadre(CategoriaResponse):
    """Categoría con info de su padre."""
    categoria_padre: Optional[CategoriaPadreResponse] = None


class CategoriaPadreConSubcategorias(CategoriaPadreResponse):
    """Categoría padre con todas sus subcategorías."""
    categorias: list[CategoriaResponse] = []


class CategoriaListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[CategoriaResponse]


class CategoriaPadreListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[CategoriaPadreResponse]