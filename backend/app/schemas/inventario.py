"""
Schemas Pydantic — Inventario
Gestión de stock de productos
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.productos import ProductoResponse


class InventarioBase(BaseModel):
    id_producto: int
    id_almacen: int
    stock: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    stock_maximo: int = Field(default=0, ge=0)


class InventarioCreate(InventarioBase):
    pass


class InventarioUpdate(BaseModel):
    stock: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    stock_maximo: Optional[int] = Field(None, ge=0)


class InventarioAjuste(BaseModel):
    cantidad: int = Field(..., description="Cantidad a agregar (positiva) o restar (negativa)")


class InventarioResponse(InventarioBase):
    model_config = ConfigDict(from_attributes=True)
    id_producto_almacen: int


class InventarioListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[InventarioResponse]