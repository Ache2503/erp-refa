"""
Schemas Pydantic — Empleados
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
import datetime


class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    direccion: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    rfc: Optional[str] = Field(None, max_length=13)
    numero_seguridad_social: Optional[str] = Field(None, max_length=20)
    cargo: Optional[str] = Field(None, max_length=50)
    estatus: str = Field(default="activo", max_length=20)


class EmpleadoCreate(EmpleadoBase):
    fecha_registro: Optional[datetime.date] = None


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    direccion: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    rfc: Optional[str] = Field(None, max_length=13)
    numero_seguridad_social: Optional[str] = Field(None, max_length=20)
    cargo: Optional[str] = Field(None, max_length=50)
    estatus: Optional[str] = Field(None, max_length=20)


class EmpleadoResponse(EmpleadoBase):
    model_config = ConfigDict(from_attributes=True)
    id_empleado: int
    fecha_registro: Optional[datetime.date] = None


class EmpleadoListResponse(BaseModel):
    """Respuesta paginada para listado de empleados."""
    total: int
    skip: int
    limit: int
    data: list[EmpleadoResponse]