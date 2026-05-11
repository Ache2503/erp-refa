from typing import Optional
from sqlalchemy.orm import Session
from app.models.ruta import Ruta
from app.models.ruta_envio import RutaEnvio

class RutaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Ruta]:
        return self.db.query(Ruta).offset(skip).limit(limit).all()

    def get_by_id(self, id_ruta: int) -> Optional[Ruta]:
        return self.db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()

    def create(self, origen: str, destino: str, distancia=None, tiempo_estimado=None) -> Ruta:
        ruta = Ruta(origen=origen, destino=destino, distancia=distancia, tiempo_estimado=tiempo_estimado)
        self.db.add(ruta)
        self.db.commit()
        self.db.refresh(ruta)
        return ruta

    def asignar_envio(self, id_ruta: int, id_envio: int) -> RutaEnvio:
        re = RutaEnvio(id_ruta=id_ruta, id_envio=id_envio)
        self.db.add(re)
        self.db.commit()
        self.db.refresh(re)
        return re
