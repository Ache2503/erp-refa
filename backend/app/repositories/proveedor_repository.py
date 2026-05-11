"""
Repository — Proveedores & Contactos
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.proveedores import Proveedores
from app.models.proveedor_contacto import ProveedorContacto
from app.schemas.proveedores import (
    ProveedorCreate, ProveedorUpdate,
    ContactoCreate, ContactoUpdate,
)


class ProveedorRepository:

    def __init__(self, db: Session):
        self.db = db

    # ── Proveedores ───────────────────────────────────────────────

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Proveedores]:
        return self.db.query(Proveedores).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Proveedores).count()

    def get_by_id(self, id_proveedor: int) -> Optional[Proveedores]:
        return self.db.query(Proveedores).filter(
            Proveedores.id_proveedor == id_proveedor
        ).first()

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Proveedores]:
        like = f"%{q}%"
        return (
            self.db.query(Proveedores)
            .filter(or_(
                Proveedores.nombre.ilike(like),
                Proveedores.email.ilike(like),
            ))
            .offset(skip).limit(limit).all()
        )

    def create(self, data: ProveedorCreate) -> Proveedores:
        proveedor = Proveedores(**data.model_dump(exclude_none=True))
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def update(self, proveedor: Proveedores, data: ProveedorUpdate) -> Proveedores:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(proveedor, field, value)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def delete(self, proveedor: Proveedores) -> None:
        self.db.delete(proveedor)
        self.db.commit()

    # ── Contactos ─────────────────────────────────────────────────

    def get_contactos(self, id_proveedor: int) -> list[ProveedorContacto]:
        return self.db.query(ProveedorContacto).filter(
            ProveedorContacto.id_proveedor == id_proveedor
        ).all()

    def get_contacto_by_id(self, id_contacto: int) -> Optional[ProveedorContacto]:
        return self.db.query(ProveedorContacto).filter(
            ProveedorContacto.id_contacto == id_contacto
        ).first()

    def create_contacto(self, id_proveedor: int,
                       data: ContactoCreate) -> ProveedorContacto:
        contacto = ProveedorContacto(
            id_proveedor=id_proveedor,
            **data.model_dump(exclude_none=True)
        )
        self.db.add(contacto)
        self.db.commit()
        self.db.refresh(contacto)
        return contacto

    def update_contacto(self, contacto: ProveedorContacto,
                        data: ContactoUpdate) -> ProveedorContacto:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contacto, field, value)
        self.db.commit()
        self.db.refresh(contacto)
        return contacto

    def delete_contacto(self, contacto: ProveedorContacto) -> None:
        self.db.delete(contacto)
        self.db.commit()