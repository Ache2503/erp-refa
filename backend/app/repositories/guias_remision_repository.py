from typing import Optional
from sqlalchemy.orm import Session
from app.models.guia_remision import GuiaRemision
from app.models.guia_remision_detalle import GuiaRemisionDetalle
from app.schemas.guias_remision import GuiaRemisionCreate

class GuiaRemisionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[GuiaRemision]:
        return self.db.query(GuiaRemision).offset(skip).limit(limit).all()

    def get_by_id(self, id_guia: int) -> Optional[GuiaRemision]:
        return self.db.query(GuiaRemision).filter(GuiaRemision.id_guia == id_guia).first()

    def create(self, data: GuiaRemisionCreate) -> GuiaRemision:
        guia = GuiaRemision(
            id_pedido_cliente=data.id_pedido_cliente,
            id_vehiculo=data.id_vehiculo,
            id_conductor=data.id_conductor,
            estatus=data.estatus,
        )
        self.db.add(guia)
        self.db.commit()
        self.db.refresh(guia)
        for d in data.detalles:
            det = GuiaRemisionDetalle(id_guia=guia.id_guia, id_producto=d.id_producto, cantidad=d.cantidad)
            self.db.add(det)
        self.db.commit()
        self.db.refresh(guia)
        return guia
