"""
Schemas Pydantic — Proveedores & Contactos
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


# ── Contacto ──────────────────────────────────────────────────────

class ContactoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class ContactoCreate(ContactoBase):
    pass


class ContactoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class ContactoResponse(ContactoBase):
    model_config = ConfigDict(from_attributes=True)
    id_contacto: int


# ── Proveedor ─────────────────────────────────────────────────────

class ProveedorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)


class ProveedorResponse(ProveedorBase):
    model_config = ConfigDict(from_attributes=True)
    id_proveedor: int


class ProveedorConContactos(ProveedorResponse):
    """Proveedor con sus contactos."""
    contactos: list[ContactoResponse] = []


class ProveedorListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[ProveedorResponse]