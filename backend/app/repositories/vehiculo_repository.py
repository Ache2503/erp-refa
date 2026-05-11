"""
Repository — Vehículos
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.vehiculo import Vehiculo
from app.schemas.vehiculos import VehiculoCreate, VehiculoUpdate


class VehiculoRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Vehiculo]:
        return self.db.query(Vehiculo).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Vehiculo).count()

    def get_by_id(self, id_vehiculo: int) -> Optional[Vehiculo]:
        return self.db.query(Vehiculo).filter(
            Vehiculo.id_vehiculo == id_vehiculo
        ).first()

    def get_by_placa(self, placa: str) -> Optional[Vehiculo]:
        return self.db.query(Vehiculo).filter(
            Vehiculo.placa == placa
        ).first()

    def get_by_conductor(self, id_conductor: int,
                         skip: int = 0, limit: int = 100) -> list[Vehiculo]:
        return (
            self.db.query(Vehiculo)
            .filter(Vehiculo.id_conductor == id_conductor)
            .offset(skip).limit(limit).all()
        )

    def get_by_tipo(self, id_tipo_vehiculo: int,
                    skip: int = 0, limit: int = 100) -> list[Vehiculo]:
        return (
            self.db.query(Vehiculo)
            .filter(Vehiculo.id_tipo_vehiculo == id_tipo_vehiculo)
            .offset(skip).limit(limit).all()
        )

    def get_by_estado(self, estado: str,
                      skip: int = 0, limit: int = 100) -> list[Vehiculo]:
        return (
            self.db.query(Vehiculo)
            .filter(Vehiculo.estado == estado)
            .offset(skip).limit(limit).all()
        )

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Vehiculo]:
        like = f"%{q}%"
        return (
            self.db.query(Vehiculo)
            .filter(Vehiculo.placa.ilike(like))
            .offset(skip).limit(limit).all()
        )

    def create(self, data: VehiculoCreate) -> Vehiculo:
        vehiculo = Vehiculo(**data.model_dump(exclude_none=True))
        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def update(self, vehiculo: Vehiculo,
               data: VehiculoUpdate) -> Vehiculo:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vehiculo, field, value)
        self.db.commit()
        self.db.refresh(vehiculo)
        return vehiculo

    def delete(self, vehiculo: Vehiculo) -> None:
        self.db.delete(vehiculo)
        self.db.commit()