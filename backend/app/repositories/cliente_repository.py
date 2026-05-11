"""
Repository — Clientes
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.clientes import Clientes
from app.schemas.clientes import ClienteCreate, ClienteUpdate


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Clientes]:
        return self.db.query(Clientes).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Clientes).count()

    def get_by_id(self, id_cliente: int) -> Optional[Clientes]:
        return self.db.query(Clientes).filter(
            Clientes.id_cliente == id_cliente
        ).first()

    def get_by_email(self, email: str) -> Optional[Clientes]:
        return self.db.query(Clientes).filter(
            Clientes.email == email
        ).first()

    def get_by_rfc(self, rfc: str) -> Optional[Clientes]:
        return self.db.query(Clientes).filter(
            Clientes.rfc == rfc
        ).first()

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Clientes]:
        like = f"%{q}%"
        return (
            self.db.query(Clientes)
            .filter(or_(
                Clientes.nombre.ilike(like),
                Clientes.apellido.ilike(like),
                Clientes.email.ilike(like),
            ))
            .offset(skip).limit(limit).all()
        )

    def filtrar_por_estatus(self, estatus: str,
                             skip: int = 0, limit: int = 100) -> list[Clientes]:
        return (
            self.db.query(Clientes)
            .filter(Clientes.estatus == estatus)
            .offset(skip).limit(limit).all()
        )

    def create(self, data: ClienteCreate) -> Clientes:
        cliente = Clientes(**data.model_dump(exclude_none=True))
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def update(self, cliente: Clientes, data: ClienteUpdate) -> Clientes:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cliente, field, value)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete(self, cliente: Clientes) -> None:
        self.db.delete(cliente)
        self.db.commit()

    def cambiar_estatus(self, cliente: Clientes, estatus: str) -> Clientes:
        cliente.estatus = estatus
        self.db.commit()
        self.db.refresh(cliente)
        return cliente