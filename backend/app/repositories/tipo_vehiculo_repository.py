"""
Repository — Tipos de Vehículos
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.tipo_vehiculo import TipoVehiculo
from app.schemas.tipos_vehiculos import (
    TipoVehiculoCreate, TipoVehiculoUpdate,
)


class TipoVehiculoRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TipoVehiculo]:
        return self.db.query(TipoVehiculo).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(TipoVehiculo).count()

    def get_by_id(self, id_tipo_vehiculo: int) -> Optional[TipoVehiculo]:
        return self.db.query(TipoVehiculo).filter(
            TipoVehiculo.id_tipo_vehiculo == id_tipo_vehiculo
        ).first()

    def get_by_nombre(self, nombre_tipo: str) -> Optional[TipoVehiculo]:
        return self.db.query(TipoVehiculo).filter(
            TipoVehiculo.nombre_tipo == nombre_tipo
        ).first()

    def create(self, data: TipoVehiculoCreate) -> TipoVehiculo:
        tv = TipoVehiculo(**data.model_dump(exclude_none=True))
        self.db.add(tv)
        self.db.commit()
        self.db.refresh(tv)
        return tv

    def update(self, tv: TipoVehiculo,
               data: TipoVehiculoUpdate) -> TipoVehiculo:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tv, field, value)
        self.db.commit()
        self.db.refresh(tv)
        return tv

    def delete(self, tv: TipoVehiculo) -> None:
        self.db.delete(tv)
        self.db.commit()