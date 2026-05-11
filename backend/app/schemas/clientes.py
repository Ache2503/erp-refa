"""
Schemas Pydantic — Clientes
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
import datetime


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    rfc: Optional[str] = Field(None, max_length=13)
    estatus: str = Field(default="activo", max_length=20)


class ClienteCreate(ClienteBase):
    fecha_registro: Optional[datetime.date] = None


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    rfc: Optional[str] = Field(None, max_length=13)
    estatus: Optional[str] = Field(None, max_length=20)


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id_cliente: int
    fecha_registro: Optional[datetime.date] = None


class ClienteListResponse(BaseModel):
    """Respuesta paginada para listado de clientes."""
    total: int
    skip: int
    limit: int
    data: list[ClienteResponse]