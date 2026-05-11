"""
Repository — Empleados
Solo acceso a datos, sin lógica de negocio.
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.empleados import Empleados
from app.schemas.empleados import EmpleadoCreate, EmpleadoUpdate


class EmpleadoRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Empleados]:
        return self.db.query(Empleados).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Empleados).count()

    def get_by_id(self, id_empleado: int) -> Optional[Empleados]:
        return self.db.query(Empleados).filter(
            Empleados.id_empleado == id_empleado
        ).first()

    def get_by_email(self, email: str) -> Optional[Empleados]:
        return self.db.query(Empleados).filter(
            Empleados.email == email
        ).first()

    def get_by_rfc(self, rfc: str) -> Optional[Empleados]:
        return self.db.query(Empleados).filter(
            Empleados.rfc == rfc
        ).first()

    def get_by_nss(self, nss: str) -> Optional[Empleados]:
        return self.db.query(Empleados).filter(
            Empleados.numero_seguridad_social == nss
        ).first()

    def buscar(self, q: str, skip: int = 0, limit: int = 100) -> list[Empleados]:
        like = f"%{q}%"
        return (
            self.db.query(Empleados)
            .filter(or_(
                Empleados.nombre.ilike(like),
                Empleados.apellido.ilike(like),
                Empleados.email.ilike(like),
                Empleados.cargo.ilike(like),
            ))
            .offset(skip).limit(limit).all()
        )

    def filtrar_por_estatus(self, estatus: str,
                             skip: int = 0, limit: int = 100) -> list[Empleados]:
        return (
            self.db.query(Empleados)
            .filter(Empleados.estatus == estatus)
            .offset(skip).limit(limit).all()
        )

    def create(self, data: EmpleadoCreate) -> Empleados:
        empleado = Empleados(**data.model_dump(exclude_none=True))
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def update(self, empleado: Empleados, data: EmpleadoUpdate) -> Empleados:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(empleado, field, value)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def delete(self, empleado: Empleados) -> None:
        self.db.delete(empleado)
        self.db.commit()

    def cambiar_estatus(self, empleado: Empleados, estatus: str) -> Empleados:
        empleado.estatus = estatus
        self.db.commit()
        self.db.refresh(empleado)
        return empleado