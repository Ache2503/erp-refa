from typing import Optional
from sqlalchemy.orm import Session
from app.models.empleados import Empleados
from app.models.empleado_rol import EmpleadoRol
from app.models.roles import Roles

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str) -> Optional[Empleados]:
        return self.db.query(Empleados).filter(Empleados.email == email).first()

    def get_roles(self, empleado_id: int) -> list[str]:
        rows = (
            self.db.query(Roles.nombre)
            .join(EmpleadoRol, EmpleadoRol.id_rol == Roles.id_rol)
            .filter(EmpleadoRol.id_empleado == empleado_id)
            .all()
        )
        return [r[0] for r in rows]

    def create_empleado(self, email: str, password_hash: str, nombre: str, apellido: str, cargo: Optional[str] = None) -> Empleados:
        emp = Empleados(
            nombre=nombre,
            apellido=apellido,
            email=email,
            cargo=cargo,
            password_hash=password_hash,
            estatus="activo",
        )
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp
