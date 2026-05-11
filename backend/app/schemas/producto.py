from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional

# Propiedades base compartidas
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    codigo: str = Field(..., min_length=1, max_length=50)
    id_categoria: int
    id_marca: int
    id_unidad_medida: int
    precio: Decimal = Field(..., ge=0)
    estatus: str = Field(default="activo")

# Esquema para crear un producto (hereda de ProductoBase)
class ProductoCreate(ProductoBase):
    pass

# Esquema para actualizar (todos los campos opcionales)
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, min_length=1, max_length=50)
    id_categoria: Optional[int] = None
    id_marca: Optional[int] = None
    id_unidad_medida: Optional[int] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    estatus: Optional[str] = None

# Esquema para respuesta (incluye id y relaciones si se desea)
class ProductoResponse(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_producto: int
    # Podrías agregar campos anidados con información de categoría/marca
    # categoria_nombre: Optional[str] = None
    # marca_nombre: Optional[str] = None