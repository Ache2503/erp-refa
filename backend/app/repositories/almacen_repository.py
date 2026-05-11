"""
Repository — Almacenes
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.almacenes import Almacenes
from app.schemas.almacenes import AlmacenCreate, AlmacenUpdate


class AlmacenRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Almacenes]:
        return self.db.query(Almacenes).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Almacenes).count()

    def get_by_id(self, id_almacen: int) -> Optional[Almacenes]:
        return self.db.query(Almacenes).filter(
            Almacenes.id_almacen == id_almacen
        ).first()

    def get_by_nombre(self, nombre: str) -> Optional[Almacenes]:
        return self.db.query(Almacenes).filter(
            Almacenes.nombre == nombre
        ).first()

    def get_by_empleado(self, id_empleado: int,
                        skip: int = 0, limit: int = 100) -> list[Almacenes]:
        return (
            self.db.query(Almacenes)
            .filter(Almacenes.id_empleado == id_empleado)
            .offset(skip).limit(limit).all()
        )

    def get_by_tipo(self, id_tipo_almacen: int,
                    skip: int = 0, limit: int = 100) -> list[Almacenes]:
        return (
            self.db.query(Almacenes)
            .filter(Almacenes.id_tipo_almacen == id_tipo_almacen)
            .offset(skip).limit(limit).all()
        )

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Almacenes]:
        like = f"%{q}%"
        return (
            self.db.query(Almacenes)
            .filter(or_(
                Almacenes.nombre.ilike(like),
                Almacenes.ubicacion.ilike(like),
            ))
            .offset(skip).limit(limit).all()
        )

    def create(self, data: AlmacenCreate) -> Almacenes:
        almacen = Almacenes(**data.model_dump(exclude_none=True))
        self.db.add(almacen)
        self.db.commit()
        self.db.refresh(almacen)
        return almacen

    def update(self, almacen: Almacenes,
               data: AlmacenUpdate) -> Almacenes:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(almacen, field, value)
        self.db.commit()
        self.db.refresh(almacen)
        return almacen

    def delete(self, almacen: Almacenes) -> None:
        self.db.delete(almacen)
        self.db.commit()