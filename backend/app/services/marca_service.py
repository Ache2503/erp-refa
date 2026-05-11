"""
Service for managing brands in the application.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from typing import List, Optional
from app.models.marcas import Marcas
from app.schemas.marcas import MarcaCreate, MarcaUpdate
from app.repositories.marca_repository import MarcaRepository


class MarcaService:
    """
    Service class for handling brand-related operations.
    """
    def __init__(self, db: Session):
        self.repo = MarcaRepository(db)

    def crear(self, data: MarcaCreate) -> Marcas:
        db_marca = Marcas(**data.model_dump())
        self.repo.create(db_marca)
        return db_marca

    def obtener(self, marca_id: int) -> Optional[Marcas]:
        return self.repo.get_by_id(marca_id)

    def listar(self) -> List[Marcas]:
        return self.repo.get_all()

    def actualizar(self, marca_id: int, data: MarcaUpdate) -> Optional[Marcas]:
        db_marca = self.obtener(marca_id)
        if not db_marca:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(db_marca, key, value)
        self.repo.update(db_marca, data)
        return db_marca

    def eliminar(self, marca_id: int) -> bool:
        db_marca = self.obtener(marca_id)
        if not db_marca:
            return False
        self.repo.delete(db_marca)
        return True