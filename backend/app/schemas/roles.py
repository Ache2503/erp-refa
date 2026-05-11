"""
Schemas Pydantic — Roles & Permisos
Validan entrada y serializan salida en los endpoints.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# ── Permiso ───────────────────────────────────────────────────────

class PermisoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = None


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = None


class PermisoResponse(PermisoBase):
    model_config = ConfigDict(from_attributes=True)
    id_permiso: int


# ── Rol ───────────────────────────────────────────────────────────

class RolBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = None


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    descripcion: Optional[str] = None


class RolResponse(RolBase):
    model_config = ConfigDict(from_attributes=True)
    id_rol: int


class RolConPermisos(RolResponse):
    """Rol con lista de permisos asignados."""
    permisos: list[PermisoResponse] = []


# ── Asignaciones ──────────────────────────────────────────────────

class AsignarPermisoRequest(BaseModel):
    """Asignar uno o varios permisos a un rol."""
    id_permisos: list[int] = Field(..., min_length=1)


class AsignarRolRequest(BaseModel):
    """Asignar un rol a un empleado."""
    id_rol: int


class EmpleadoRolResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_empleado_rol: int
    id_empleado: int
    id_rol: int
    rol: RolResponse