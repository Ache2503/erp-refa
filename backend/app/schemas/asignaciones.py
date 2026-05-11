from pydantic import BaseModel
from typing import Optional

class AsignacionCreate(BaseModel):
    id_pedido_cliente: int
    id_vehiculo: int
    id_conductor: int
    origen: Optional[str] = None
    destino: Optional[str] = None

class AsignacionResponse(BaseModel):
    id_pedido_cliente: int
    id_envio: int
    id_guia: int
    id_ruta: Optional[int] = None
    estatus: str
    mensaje: str
