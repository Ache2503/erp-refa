"""
Service — Logística / Envíos
Maneja envíos de pedidos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.envio_repository import EnvioRepository
from app.repositories.pedido_cliente_repository import PedidoClienteRepository
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.logistica import (
    EnvioCreate, EnvioUpdate,
    EnvioResponse, EnvioConDetalles, EnvioListResponse,
)


class LogisticaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EnvioRepository(db)
        self.pedido_repo = PedidoClienteRepository(db)
        self.vehiculo_repo = VehiculoRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> EnvioListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return EnvioListResponse(
            total=total, skip=skip, limit=limit,
            data=[EnvioResponse.model_validate(e) for e in data],
        )

    def obtener(self, id_envio: int) -> EnvioConDetalles:
        envio = self.repo.get_by_id(id_envio)
        if not envio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Envío {id_envio} no encontrado",
            )
        return EnvioConDetalles.model_validate(envio)

    def crear(self, data: EnvioCreate) -> EnvioResponse:
        if not self.pedido_repo.get_by_id(data.id_pedido_cliente):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {data.id_pedido_cliente} no existe",
            )
        if not self.vehiculo_repo.get_by_id(data.id_vehiculo):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {data.id_vehiculo} no existe",
            )
        if not self.empleado_repo.get_by_id(data.id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {data.id_empleado} no existe",
            )
        
        return EnvioResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_envio: int,
                  data: EnvioUpdate) -> EnvioResponse:
        envio = self.repo.get_by_id(id_envio)
        if not envio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Envío {id_envio} no encontrado",
            )
        return EnvioResponse.model_validate(self.repo.update(envio, data))

    def eliminar(self, id_envio: int) -> None:
        envio = self.repo.get_by_id(id_envio)
        if not envio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Envío {id_envio} no encontrado",
            )
        self.repo.delete(envio)

    def listar_por_estado(self, estado: str, skip: int = 0,
                      limit: int = 100) -> list[EnvioResponse]:
        return [
            EnvioResponse.model_validate(e)
            for e in self.repo.get_by_estado(estado, skip, limit)
        ]

    def listar_por_vehiculo(self, id_vehiculo: int, skip: int = 0,
                          limit: int = 100) -> list[EnvioResponse]:
        if not self.vehiculo_repo.get_by_id(id_vehiculo):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {id_vehiculo} no existe",
            )
        return [
            EnvioResponse.model_validate(e)
            for e in self.repo.get_by_vehiculo(id_vehiculo, skip, limit)
        ]

    def listar_por_empleado(self, id_empleado: int, skip: int = 0,
                          limit: int = 100) -> list[EnvioResponse]:
        if not self.empleado_repo.get_by_id(id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no existe",
            )
        return [
            EnvioResponse.model_validate(e)
            for e in self.repo.get_by_empleado(id_empleado, skip, limit)
        ]