from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.conductores import Conductores
from app.models.empleados import Empleados
from app.models.envios import Envios

class ConductorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[dict]:
        return (
            self.db.query(Conductores, Empleados)
            .join(Empleados, Empleados.id_empleado == Conductores.id_empleado)
            .all()
        )

    def get_disponibles(self) -> list[dict]:
        subquery = (
            self.db.query(Envios.id_empleado)
            .filter(Envios.estatus.in_(["pendiente", "en_transito"]))
            .subquery()
        )
        return (
            self.db.query(Conductores, Empleados)
            .join(Empleados, Empleados.id_empleado == Conductores.id_empleado)
            .filter(Empleados.estatus == "activo")
            .filter(~Conductores.id_empleado.in_(subquery))
            .all()
        )

    def get_by_id(self, id_empleado: int) -> Optional[Conductores]:
        return self.db.query(Conductores).filter(Conductores.id_empleado == id_empleado).first()
