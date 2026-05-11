"""
Repository — Logística / Envíos
Maneja envíos de pedidos
"""
from typing import Optional
from sqlalchemy.orm import Session
from decimal import Decimal

from app.models.envios import Envios
from app.models.envio_detalle import EnvioDetalle
from app.schemas.logistica import (
    EnvioCreate, EnvioUpdate,
)


class EnvioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Envios]:
        return self.db.query(Envios).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Envios).count()

    def get_by_id(self, id_envio: int) -> Optional[Envios]:
        return self.db.query(Envios).filter(Envios.id_envio == id_envio).first()

    def get_by_pedido(self, id_pedido: int) -> Optional[Envios]:
        return self.db.query(Envios).filter(Envios.id_pedido_cliente == id_pedido).first()

    def get_by_estado(self, estado: str, skip: int = 0,
                   limit: int = 100) -> list[Envios]:
        return (
            self.db.query(Envios)
            .filter(Envios.estatus == estado)
            .offset(skip).limit(limit).all()
        )

    def get_by_vehiculo(self, id_vehiculo: int, skip: int = 0,
                     limit: int = 100) -> list[Envios]:
        return (
            self.db.query(Envios)
            .filter(Envios.id_vehiculo == id_vehiculo)
            .offset(skip).limit(limit).all()
        )

    def get_by_empleado(self, id_empleado: int, skip: int = 0,
                     limit: int = 100) -> list[Envios]:
        return (
            self.db.query(Envios)
            .filter(Envios.id_empleado == id_empleado)
            .offset(skip).limit(limit).all()
        )

    def create(self, data: EnvioCreate) -> Envios:
        envio = Envios(
            id_pedido_cliente=data.id_pedido_cliente,
            id_vehiculo=data.id_vehiculo,
            id_empleado=data.id_empleado,
            estatus=data.estatus or "pendiente",
        )
        self.db.add(envio)
        self.db.commit()
        self.db.refresh(envio)
        return envio

    def update(self, envio: Envios,
             data: EnvioUpdate) -> Envios:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(envio, field, value)
        self.db.commit()
        self.db.refresh(envio)
        return envio

    def delete(self, envio: Envios) -> None:
        self.db.delete(envio)
        self.db.commit()

    def get_detalles(self, id_envio: int) -> list[EnvioDetalle]:
        return self.db.query(EnvioDetalle).filter(
            EnvioDetalle.id_envio == id_envio
        ).all()

    def create_detalle(self, id_envio: int, id_producto: int,
                     cantidad: int) -> EnvioDetalle:
        from app.models.envio_detalle import EnvioDetalle
        detalle = EnvioDetalle(
            id_envio=id_envio,
            id_producto=id_producto,
            cantidad=cantidad,
        )
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def delete_detalle(self, detalle: EnvioDetalle) -> None:
        self.db.delete(detalle)
        self.db.commit()