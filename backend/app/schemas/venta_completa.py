from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class VentaCompletaDetalle(BaseModel):
    id_producto: int
    cantidad: int = Field(..., ge=1)
    precio_unitario: Decimal = Field(..., ge=0)

class VentaCompletaEnvio(BaseModel):
    requiere_envio: bool = False
    id_vehiculo: Optional[int] = None
    id_conductor: Optional[int] = None
    origen: Optional[str] = None
    destino: Optional[str] = None

class VentaCompletaRequest(BaseModel):
    id_cliente: int
    id_empleado: int
    id_almacen: int = 1
    detalles: list[VentaCompletaDetalle]
    envio: VentaCompletaEnvio = VentaCompletaEnvio()

class VentaCompletaResponse(BaseModel):
    id_pedido: int
    total: Decimal
    estatus: str
    id_envio: Optional[int] = None
    id_guia: Optional[int] = None
    ticket: dict
