"""
Repository — Marcas
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.marcas import Marcas
from app.schemas.marcas import MarcaCreate, MarcaUpdate


class MarcaRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Marcas]:
        return self.db.query(Marcas).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Marcas).count()

    def get_by_id(self, id_marca: int) -> Optional[Marcas]:
        return self.db.query(Marcas).filter(Marcas.id_marca == id_marca).first()

    def get_by_nombre(self, nombre: str) -> Optional[Marcas]:
        return self.db.query(Marcas).filter(Marcas.nombre == nombre).first()

    def create(self, marca: Marcas) -> Marcas:
        self.db.add(marca)
        self.db.commit()
        self.db.refresh(marca)
        return marca

    def update(self, marca: Marcas, data: MarcaUpdate) -> Marcas:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(marca, field, value)
        self.db.commit()
        self.db.refresh(marca)
        return marca

    def delete(self, marca: Marcas) -> None:
        self.db.delete(marca)
        self.db.commit()

    def list(self) -> list[Marcas]:
        return self.db.query(Marcas).all()
    