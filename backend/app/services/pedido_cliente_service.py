"""
Service — Pedidos Clientes
Maneja órdenes de venta a clientes
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.repositories.pedido_cliente_repository import PedidoClienteRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.almacen_repository import AlmacenRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.pedidos_clientes import (
    PedidoClienteCreate, PedidoClienteUpdate,
    PedidoClienteResponse, PedidoClienteConDetalles, 
    PedidoClienteListResponse,
    PedidoClienteDetalleResponse,
)


class PedidoClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PedidoClienteRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.almacen_repo = AlmacenRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> PedidoClienteListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return PedidoClienteListResponse(
            total=total, skip=skip, limit=limit,
            data=[PedidoClienteResponse.model_validate(p) for p in data],
        )

    def obtener(self, id_pedido: int) -> PedidoClienteConDetalles:
        pedido = self.repo.get_by_id(id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {id_pedido} no encontrado",
            )
        return PedidoClienteConDetalles.model_validate(pedido)

    def crear(self, data: PedidoClienteCreate) -> PedidoClienteResponse:
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
        if not self.almacen_repo.get_by_id(data.id_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {data.id_almacen} no existe",
            )
        
        return PedidoClienteResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_pedido: int, 
                  data: PedidoClienteUpdate) -> PedidoClienteResponse:
        pedido = self.repo.get_by_id(id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {id_pedido} no encontrado",
            )
        return PedidoClienteResponse.model_validate(self.repo.update(pedido, data))

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.repo.get_by_id(id_pedido)
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {id_pedido} no encontrado",
            )
        self.repo.delete(pedido)

    def listar_detalles(self, id_pedido: int) -> list[PedidoClienteDetalleResponse]:
        if not self.repo.get_by_id(id_pedido):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido {id_pedido} no encontrado",
            )
        return [
            PedidoClienteDetalleResponse.model_validate(d)
            for d in self.repo.get_detalles(id_pedido)
        ]

    def obtener_detalle(self, id_detalle: int) -> PedidoClienteDetalleResponse:
        detalle = self.repo.get_detalle_by_id(id_detalle)
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detalle {id_detalle} no encontrado",
            )
        return PedidoClienteDetalleResponse.model_validate(detalle)

    def eliminar_detalle(self, id_detalle: int) -> None:
        detalle = self.repo.get_detalle_by_id(id_detalle)
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detalle {id_detalle} no encontrado",
            )
        self.repo.delete_detalle(detalle)

    def listar_por_cliente(self, id_cliente: int, 
                          skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        if not self.cliente_repo.get_by_id(id_cliente):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no existe",
            )
        return [
            PedidoClienteResponse.model_validate(p)
            for p in self.repo.get_by_cliente(id_cliente, skip, limit)
        ]

    def listar_por_estado(self, estado: str, 
                         skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        return [
            PedidoClienteResponse.model_validate(p)
            for p in self.repo.get_by_estado(estado, skip, limit)
        ]

    def listar_por_empleado(self, id_empleado: int, 
                           skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        if not self.empleado_repo.get_by_id(id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no existe",
            )
        return [
            PedidoClienteResponse.model_validate(p)
            for p in self.repo.get_by_empleado(id_empleado, skip, limit)
        ]