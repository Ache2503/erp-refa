"""
Service — Ventas
Maneja ventas directas
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.venta_repository import VentaRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.ventas import (
    VentaCreate, VentaUpdate,
    VentaResponse, VentaConDetalles, VentaListResponse,
)


class VentaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = VentaRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> VentaListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return VentaListResponse(
            total=total, skip=skip, limit=limit,
            data=[VentaResponse.model_validate(v) for v in data],
        )

    def obtener(self, id_venta: int) -> VentaConDetalles:
        venta = self.repo.get_by_id(id_venta)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta {id_venta} no encontrada",
            )
        return VentaConDetalles.model_validate(venta)

    def crear(self, data: VentaCreate) -> VentaResponse:
        if not self.cliente_repo.get_by_id(data.id_cliente):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {data.id_cliente} no existe",
            )
        if not self.empleado_repo.get_by_id(data.id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {data.id_empleado} no existe",
            )
        
        return VentaResponse.model_validate(
            self.repo.create(data.id_cliente, data.id_empleado, data.id_almacen)
        )

    def actualizar(self, id_venta: int,
                  data: VentaUpdate) -> VentaResponse:
        venta = self.repo.get_by_id(id_venta)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta {id_venta} no encontrada",
            )
        return VentaResponse.model_validate(self.repo.update(venta, data.estatus or venta.estatus))

    def eliminar(self, id_venta: int) -> None:
        venta = self.repo.get_by_id(id_venta)
        if not venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta {id_venta} no encontrada",
            )
        self.repo.delete(venta)

    def listar_por_cliente(self, id_cliente: int,
                        skip: int = 0, limit: int = 100) -> list[VentaResponse]:
        if not self.cliente_repo.get_by_id(id_cliente):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no existe",
            )
        return [
            VentaResponse.model_validate(v)
            for v in self.repo.get_by_cliente(id_cliente, skip, limit)
        ]

    def listar_por_estado(self, estado: str,
                     skip: int = 0, limit: int = 100) -> list[VentaResponse]:
        return [
            VentaResponse.model_validate(v)
            for v in self.repo.get_by_estado(estado, skip, limit)
        ]