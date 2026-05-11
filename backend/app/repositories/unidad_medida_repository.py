"""
Repository — Unidades de Medida
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.unidades_medida import UnidadesMedida
from app.schemas.unidades_medida import (
    UnidadMedidaCreate, UnidadMedidaUpdate,
)


class UnidadMedidaRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UnidadesMedida]:
        return self.db.query(UnidadesMedida).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(UnidadesMedida).count()

    def get_by_id(self, id_unidad_medida: int) -> Optional[UnidadesMedida]:
        return self.db.query(UnidadesMedida).filter(
            UnidadesMedida.id_unidad_medida == id_unidad_medida
        ).first()

    def get_by_nombre(self, nombre: str) -> Optional[UnidadesMedida]:
        return self.db.query(UnidadesMedida).filter(
            UnidadesMedida.nombre == nombre
        ).first()

    def get_by_abreviatura(self, abreviatura: str) -> Optional[UnidadesMedida]:
        return self.db.query(UnidadesMedida).filter(
            UnidadesMedida.abreviatura == abreviatura
        ).first()

    def create(self, data: UnidadMedidaCreate) -> UnidadesMedida:
        um = UnidadesMedida(**data.model_dump())
        self.db.add(um)
        self.db.commit()
        self.db.refresh(um)
        return um

    def update(self, um: UnidadesMedida,
               data: UnidadMedidaUpdate) -> UnidadesMedida:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(um, field, value)
        self.db.commit()
        self.db.refresh(um)
        return um

    def delete(self, um: UnidadesMedida) -> None:
        self.db.delete(um)
        self.db.commit()