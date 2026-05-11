from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.rutas_repository import RutaRepository
from app.schemas.rutas import RutaCreate, RutaResponse

class RutaService:
    def __init__(self, db: Session):
        self.repo = RutaRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> list[RutaResponse]:
        return [RutaResponse.model_validate(r) for r in self.repo.get_all(skip, limit)]

    def crear(self, data: RutaCreate) -> RutaResponse:
        return RutaResponse.model_validate(
            self.repo.create(data.origen, data.destino, data.distancia, data.tiempo_estimado)
        )

    def asignar_envio(self, id_ruta: int, id_envio: int):
        ruta = self.repo.get_by_id(id_ruta)
        if not ruta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruta no encontrada")
        self.repo.asignar_envio(id_ruta, id_envio)
        return {"mensaje": "Ruta asignada al envío"}
