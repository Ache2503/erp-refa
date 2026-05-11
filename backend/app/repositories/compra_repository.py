"""
Repository — Compras
Acceso a datos para órdenes de compra.
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.compras import Compras
from app.models.compra_detalle import CompraDetalle
from app.schemas.compras import CompraCreate, CompraUpdate


class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Compras]:
        return self.db.query(Compras).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Compras).count()

    def get_by_id(self, id_compra: int) -> Optional[Compras]:
        return self.db.query(Compras).filter(
            Compras.id_compra == id_compra
        ).first()

    def get_by_numero_orden(self, numero_orden: str) -> Optional[Compras]:
        return self.db.query(Compras).filter(
            Compras.numero_orden == numero_orden
        ).first()

    def get_by_proveedor(self, id_proveedor: int, 
                        skip: int = 0, limit: int = 100) -> list[Compras]:
        return (
            self.db.query(Compras)
            .filter(Compras.id_proveedor == id_proveedor)
            .offset(skip).limit(limit).all()
        )

    def get_by_estado(self, estado: str, 
                     skip: int = 0, limit: int = 100) -> list[Compras]:
        return (
            self.db.query(Compras)
            .filter(Compras.estado == estado)
            .offset(skip).limit(limit).all()
        )

    def get_by_empleado(self, id_empleado: int, 
                       skip: int = 0, limit: int = 100) -> list[Compras]:
        return (
            self.db.query(Compras)
            .filter(Compras.id_empleado == id_empleado)
            .offset(skip).limit(limit).all()
        )

    def buscar(self, q: str, skip: int = 0, 
              limit: int = 100) -> list[Compras]:
        like = f"%{q}%"
        return (
            self.db.query(Compras)
            .filter(Compras.numero_orden.ilike(like))
            .offset(skip).limit(limit).all()
        )

    def create(self, data: CompraCreate) -> Compras:
        compra = Compras(**data.model_dump(exclude=['detalles']))
        self.db.add(compra)
        self.db.flush()
        
        # Crear detalles
        for det_data in data.detalles:
            detalle = CompraDetalle(**det_data.model_dump(), id_compra=compra.id_compra)
            self.db.add(detalle)
        
        self.db.commit()
        self.db.refresh(compra)
        return compra

    def update(self, compra: Compras, data: CompraUpdate) -> Compras:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(compra, field, value)
        self.db.commit()
        self.db.refresh(compra)
        return compra

    def delete(self, compra: Compras) -> None:
        self.db.delete(compra)
        self.db.commit()


class CompraDetalleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_compra_detalle: int) -> Optional[CompraDetalle]:
        return self.db.query(CompraDetalle).filter(
            CompraDetalle.id_compra_detalle == id_compra_detalle
        ).first()

    def get_by_compra(self, id_compra: int) -> list[CompraDetalle]:
        return self.db.query(CompraDetalle).filter(
            CompraDetalle.id_compra == id_compra
        ).all()

    def delete(self, detalle: CompraDetalle) -> None:
        self.db.delete(detalle)
        self.db.commit()