from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ConductorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_empleado: int
    licencia_conducir: str
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    cargo: Optional[str] = None
    estatus: str

class ConductorDisponibleResponse(BaseModel):
    id_empleado: int
    nombre_completo: str
    licencia: str
    telefono: Optional[str] = None
