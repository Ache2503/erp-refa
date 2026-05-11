"""
Repository — Categorías
Maneja categoria_padre y categorias (subcategorías)
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.categoria_padre import CategoriaPadre
from app.models.categorias import Categorias
from app.schemas.categorias import (
    CategoriaPadreCreate, CategoriaPadreUpdate,
    CategoriaCreate, CategoriaUpdate,
)


class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db

    # ── Categoría Padre ───────────────────────────────────────────

    def get_all_padres(self, skip: int = 0, limit: int = 100) -> list[CategoriaPadre]:
        return self.db.query(CategoriaPadre).offset(skip).limit(limit).all()

    def get_total_padres(self) -> int:
        return self.db.query(CategoriaPadre).count()

    def get_padre_by_id(self, id_categoria_padre: int) -> Optional[CategoriaPadre]:
        return self.db.query(CategoriaPadre).filter(
            CategoriaPadre.id_categoria_padre == id_categoria_padre
        ).first()

    def get_padre_by_nombre(self, nombre: str) -> Optional[CategoriaPadre]:
        return self.db.query(CategoriaPadre).filter(
            CategoriaPadre.nombre == nombre
        ).first()

    def create_padre(self, data: CategoriaPadreCreate) -> CategoriaPadre:
        padre = CategoriaPadre(**data.model_dump(exclude_none=True))
        self.db.add(padre)
        self.db.commit()
        self.db.refresh(padre)
        return padre

    def update_padre(self, padre: CategoriaPadre,
                     data: CategoriaPadreUpdate) -> CategoriaPadre:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(padre, field, value)
        self.db.commit()
        self.db.refresh(padre)
        return padre

    def delete_padre(self, padre: CategoriaPadre) -> None:
        self.db.delete(padre)
        self.db.commit()

    # ── Categoría (Subcategoría) ──────────────────────────────────

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Categorias]:
        return self.db.query(Categorias).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Categorias).count()

    def get_by_id(self, id_categoria: int) -> Optional[Categorias]:
        return self.db.query(Categorias).filter(
            Categorias.id_categoria == id_categoria
        ).first()

    def get_by_nombre(self, nombre: str) -> Optional[Categorias]:
        return self.db.query(Categorias).filter(
            Categorias.nombre == nombre
        ).first()

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Categorias]:
        like = f"%{q}%"
        return (
            self.db.query(Categorias)
            .filter(or_(
                Categorias.nombre.ilike(like),
                Categorias.descripcion.ilike(like),
            ))
            .offset(skip).limit(limit).all()
        )

    def get_by_padre(self, id_categoria_padre: int,
                      skip: int = 0, limit: int = 100) -> list[Categorias]:
        return (
            self.db.query(Categorias)
            .filter(Categorias.id_categoria_padre == id_categoria_padre)
            .offset(skip).limit(limit).all()
        )

    def create(self, data: CategoriaCreate) -> Categorias:
        categoria = Categorias(**data.model_dump(exclude_none=True))
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def update(self, categoria: Categorias,
               data: CategoriaUpdate) -> Categorias:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(categoria, field, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, categoria: Categorias) -> None:
        self.db.delete(categoria)
        self.db.commit()