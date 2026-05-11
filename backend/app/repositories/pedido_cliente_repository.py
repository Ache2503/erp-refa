"""
Repository — Pedidos Clientes
Maneja pedidos (órdenes de venta) y sus detalles
"""
from typing import Optional
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.pedidos_clientes import PedidosClientes
from app.models.pedido_cliente_detalle import PedidoClienteDetalle
from app.schemas.pedidos_clientes import (
    PedidoClienteCreate, PedidoClienteUpdate,
)


class PedidoClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PedidosClientes]:
        return self.db.query(PedidosClientes).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(PedidosClientes).count()

    def get_by_id(self, id_pedido: int) -> Optional[PedidosClientes]:
        return self.db.query(PedidosClientes).filter(
            PedidosClientes.id_pedido_cliente == id_pedido
        ).first()

    def get_by_cliente(self, id_cliente: int, skip: int = 0, 
                   limit: int = 100) -> list[PedidosClientes]:
        return (
            self.db.query(PedidosClientes)
            .filter(PedidosClientes.id_cliente == id_cliente)
            .offset(skip).limit(limit).all()
        )

    def get_by_empleado(self, id_empleado: int, skip: int = 0,
                    limit: int = 100) -> list[PedidosClientes]:
        return (
            self.db.query(PedidosClientes)
            .filter(PedidosClientes.id_empleado == id_empleado)
            .offset(skip).limit(limit).all()
        )

    def get_by_estado(self, estado: str, skip: int = 0,
                   limit: int = 100) -> list[PedidosClientes]:
        return (
            self.db.query(PedidosClientes)
            .filter(PedidosClientes.estatus == estado)
            .offset(skip).limit(limit).all()
        )

    def create(self, data: PedidoClienteCreate) -> PedidosClientes:
        pedido = PedidosClientes(
            id_cliente=data.id_cliente,
            id_empleado=data.id_empleado,
            id_almacen=data.id_almacen,
            subtotal=Decimal("0.00"),
            impuesto=Decimal("0.00"),
            total=Decimal("0.00"),
            estatus=data.estatus or "pendiente",
        )
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def update(self, pedido: PedidosClientes,
             data: PedidoClienteUpdate) -> PedidosClientes:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(pedido, field, value)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def delete(self, pedido: PedidosClientes) -> None:
        self.db.delete(pedido)
        self.db.commit()

    def get_detalles(self, id_pedido: int) -> list[PedidoClienteDetalle]:
        return self.db.query(PedidoClienteDetalle).filter(
            PedidoClienteDetalle.id_pedido_cliente == id_pedido
        ).all()

    def get_detalle_by_id(self, id_detalle: int) -> Optional[PedidoClienteDetalle]:
        return self.db.query(PedidoClienteDetalle).filter(
            PedidoClienteDetalle.id_pedido_cliente_detalle == id_detalle
        ).first()

    def delete_detalle(self, detalle: PedidoClienteDetalle) -> None:
        self.db.delete(detalle)
        self.db.commit()