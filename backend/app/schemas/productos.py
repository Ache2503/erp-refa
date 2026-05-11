"""
Schemas Pydantic — Productos
Relaciones: categorias + marcas + unidades_medida
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal

from app.schemas.categorias import CategoriaResponse
from app.schemas.marcas import MarcaResponse
from app.schemas.unidades_medida import UnidadMedidaResponse


class ProductoBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50, description="Código único del producto")
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None
    id_categoria: int
    id_marca: Optional[int] = None
    id_unidad_medida: int
    precio_compra: Decimal = Field(..., gt=0, decimal_places=2)
    precio_venta: Decimal = Field(..., gt=0, decimal_places=2)
    margen_ganancia: Optional[Decimal] = Field(None, description="% margen (calculado)")
    peso: Optional[Decimal] = Field(None, gt=0, description="Peso en kg")
    estado: str = Field(default="activo", description="activo, descontinuado, en_desarrollo")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    id_marca: Optional[int] = None
    id_unidad_medida: Optional[int] = None
    precio_compra: Optional[Decimal] = Field(None, gt=0)
    precio_venta: Optional[Decimal] = Field(None, gt=0)
    peso: Optional[Decimal] = Field(None, gt=0)
    estado: Optional[str] = None


class ProductoResponse(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id_producto: int


class ProductoConRelaciones(ProductoResponse):
    """Producto con datos de categoría, marca y unidad."""
    categoria: Optional[CategoriaResponse] = None
    marca: Optional[MarcaResponse] = None
    unidad_medida: Optional[UnidadMedidaResponse] = None


class ProductoListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[ProductoResponse]