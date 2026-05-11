"""
Repository — Ventas
Maneja ventas directas (sin pedido)
"""
from typing import Optional
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.pedidos_clientes import PedidosClientes
from app.models.pedido_cliente_detalle import PedidoClienteDetalle


class VentaRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PedidosClientes]:
        return self.db.query(PedidosClientes).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(PedidosClientes).count()

    def get_by_id(self, id_venta: int) -> Optional[PedidosClientes]:
        return self.db.query(PedidosClientes).filter(
            PedidosClientes.id_pedido_cliente == id_venta
        ).first()

    def get_by_cliente(self, id_cliente: int, skip: int = 0, 
                   limit: int = 100) -> list[PedidosClientes]:
        return (
            self.db.query(PedidosClientes)
            .filter(PedidosClientes.id_cliente == id_cliente)
            .offset(skip).limit(limit).all()
        )

    def get_by_estado(self, estado: str, skip: int = 0,
                   limit: int = 100) -> list[PedidosClientes]:
        return (
            self.db.query(PedidosClientes)
            .filter(PedidosClientes.estatus == estado)
            .offset(skip).limit(limit).all()
        )

    def create(self, id_cliente: int, id_empleado: int, 
              id_almacen: int = None) -> PedidosClientes:
        from datetime import datetime
        
        # Buscar cualquier almacen disponible
        from app.models.almacenes import Almacenes
        almacen = self.db.query(Almacenes).first()
        almacen_id = almacen.id_almacen if almacen else 1
        
        venta = PedidosClientes(
            id_cliente=id_cliente,
            id_empleado=id_empleado,
            id_almacen=almacen_id,
            subtotal=Decimal("0.00"),
            impuesto=Decimal("0.00"),
            total=Decimal("0.00"),
            estatus="completado",
        )
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def update(self, venta: PedidosClientes, estatus: str) -> PedidosClientes:
        venta.estatus = estatus
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def delete(self, venta: PedidosClientes) -> None:
        self.db.delete(venta)
        self.db.commit()