from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date

class GuiaDetalleCreate(BaseModel):
    id_producto: int
    cantidad: int = Field(..., ge=1)

class GuiaRemisionCreate(BaseModel):
    id_pedido_cliente: int
    id_vehiculo: int
    id_conductor: int
    estatus: str = Field(default="emitida")
    detalles: list[GuiaDetalleCreate] = []

class GuiaRemisionDetalleFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_producto: int
    producto: str
    codigo: str
    cantidad: int

class GuiaVehiculoInfo(BaseModel):
    id_vehiculo: int
    placa: str
    marca: str
    modelo: Optional[str] = None
    capacidad_carga: Optional[float] = None

class GuiaVendedorInfo(BaseModel):
    id_empleado: int
    nombre: str
    apellido: str

class GuiaClienteInfo(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str

class GuiaAlmacenInfo(BaseModel):
    id_almacen: int
    nombre: str

class GuiaRemisionFullResponse(BaseModel):
    id_guia: int
    id_pedido_cliente: int
    id_conductor: int
    fecha_guia: date
    estatus: str
    vendedor: GuiaVendedorInfo
    cliente: GuiaClienteInfo
    almacen: GuiaAlmacenInfo
    vehiculo: GuiaVehiculoInfo
    detalles: list[GuiaRemisionDetalleFull]

class GuiaRemisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_guia: int
    id_pedido_cliente: int
    fecha_guia: date
    id_vehiculo: int
    id_conductor: int
    estatus: str
