from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.productos import Productos  # Ajusta el nombre de la clase según tu modelo
from app.schemas.producto import ProductoCreate, ProductoUpdate

class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, producto_id: int) -> Optional[Productos]:
        return self.db.query(Productos).filter(Productos.id_producto == producto_id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Productos]:
        return self.db.query(Productos).filter(Productos.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Productos]:
        return self.db.query(Productos).offset(skip).limit(limit).all()

    def create(self, producto_data: ProductoCreate) -> Productos:
        db_producto = Productos(**producto_data.model_dump())
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto

    def update(self, producto: Productos, update_data: ProductoUpdate) -> Productos:
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(producto, field, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, producto: Productos) -> None:
        self.db.delete(producto)
        self.db.commit()
