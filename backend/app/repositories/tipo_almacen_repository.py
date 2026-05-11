"""
Repository — Tipos de Almacén
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.tipos_almacen import TiposAlmacen
from app.schemas.tipos_almacen import (
    TipoAlmacenCreate, TipoAlmacenUpdate,
)


class TipoAlmacenRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[TiposAlmacen]:
        return self.db.query(TiposAlmacen).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(TiposAlmacen).count()

    def get_by_id(self, id_tipo_almacen: int) -> Optional[TiposAlmacen]:
        return self.db.query(TiposAlmacen).filter(
            TiposAlmacen.id_tipo_almacen == id_tipo_almacen
        ).first()

    def get_by_nombre(self, nombre: str) -> Optional[TiposAlmacen]:
        return self.db.query(TiposAlmacen).filter(
            TiposAlmacen.nombre == nombre
        ).first()

    def create(self, data: TipoAlmacenCreate) -> TiposAlmacen:
        ta = TiposAlmacen(**data.model_dump(exclude_none=True))
        self.db.add(ta)
        self.db.commit()
        self.db.refresh(ta)
        return ta

    def update(self, ta: TiposAlmacen,
               data: TipoAlmacenUpdate) -> TiposAlmacen:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(ta, field, value)
        self.db.commit()
        self.db.refresh(ta)
        return ta

    def delete(self, ta: TiposAlmacen) -> None:
        self.db.delete(ta)
        self.db.commit()