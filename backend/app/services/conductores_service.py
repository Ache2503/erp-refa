from sqlalchemy.orm import Session
from app.repositories.conductores_repository import ConductorRepository
from app.schemas.conductores import ConductorResponse, ConductorDisponibleResponse

class ConductorService:
    def __init__(self, db: Session):
        self.repo = ConductorRepository(db)

    def listar(self) -> list[ConductorResponse]:
        rows = self.repo.get_all()
        result = []
        for c, e in rows:
            result.append(ConductorResponse(
                id_empleado=c.id_empleado,
                licencia_conducir=c.licencia_conducir,
                nombre=e.nombre,
                apellido=e.apellido,
                email=e.email,
                telefono=e.telefono,
                cargo=e.cargo,
                estatus=e.estatus,
            ))
        return result

    def disponibles(self) -> list[ConductorDisponibleResponse]:
        rows = self.repo.get_disponibles()
        result = []
        for c, e in rows:
            result.append(ConductorDisponibleResponse(
                id_empleado=c.id_empleado,
                nombre_completo=f"{e.nombre} {e.apellido}",
                licencia=c.licencia_conducir,
                telefono=e.telefono,
            ))
        return result
