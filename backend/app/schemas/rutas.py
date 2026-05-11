from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
import datetime

class RutaCreate(BaseModel):
    origen: str = Field(..., min_length=1)
    destino: str = Field(..., min_length=1)
    distancia: Optional[Decimal] = None
    tiempo_estimado: Optional[str] = None

class RutaEnvioCreate(BaseModel):
    id_ruta: int
    id_envio: int

class RutaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_ruta: int
    origen: str
    destino: str
    distancia: Optional[Decimal] = None
    tiempo_estimado: Optional[str] = None

    @classmethod
    def model_validate(cls, obj):
        if hasattr(obj, 'tiempo_estimado') and isinstance(obj.tiempo_estimado, datetime.time):
            obj.tiempo_estimado = obj.tiempo_estimado.strftime('%H:%M:%S')
        return super().model_validate(obj)
