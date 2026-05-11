"""
Repository — Inventario
Gestiona stock de productos en almacenes
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.productos_almacen import ProductosAlmacen


class InventarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductosAlmacen]:
        return self.db.query(ProductosAlmacen).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(ProductosAlmacen).count()

    def get_by_id(self, id: int) -> Optional[ProductosAlmacen]:
        return self.db.query(ProductosAlmacen).filter(
            ProductosAlmacen.id_producto_almacen == id
        ).first()

    def get_by_producto(self, id_producto: int, skip: int = 0, 
                       limit: int = 100) -> list[ProductosAlmacen]:
        return (
            self.db.query(ProductosAlmacen)
            .filter(ProductosAlmacen.id_producto == id_producto)
            .offset(skip).limit(limit).all()
        )

    def get_by_almacen(self, id_almacen: int, skip: int = 0,
                      limit: int = 100) -> list[ProductosAlmacen]:
        return (
            self.db.query(ProductosAlmacen)
            .filter(ProductosAlmacen.id_almacen == id_almacen)
            .offset(skip).limit(limit).all()
        )

    def get_by_producto_almacen(self, id_producto: int, 
                                 id_almacen: int) -> Optional[ProductosAlmacen]:
        return self.db.query(ProductosAlmacen).filter(
            ProductosAlmacen.id_producto == id_producto,
            ProductosAlmacen.id_almacen == id_almacen
        ).first()

    def get_bajo_stock(self, skip: int = 0, limit: int = 100) -> list[ProductosAlmacen]:
        return (
            self.db.query(ProductosAlmacen)
            .filter(ProductosAlmacen.stock <= ProductosAlmacen.stock_minimo)
            .offset(skip).limit(limit).all()
        )

    def create(self, id_producto: int, id_almacen: int, 
             stock: int = 0, stock_minimo: int = 0, 
             stock_maximo: int = 0) -> ProductosAlmacen:
        inventario = ProductosAlmacen(
            id_producto=id_producto,
            id_almacen=id_almacen,
            stock=stock,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
        )
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def update_stock(self, inventario: ProductosAlmacen, 
                   stock: int) -> ProductosAlmacen:
        inventario.stock = stock
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def ajustar_stock(self, inventario: ProductosAlmacen, 
                     cantidad: int) -> ProductosAlmacen:
        inventario.stock += cantidad
        if inventario.stock < 0:
            inventario.stock = 0
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def delete(self, inventario: ProductosAlmacen) -> None:
        self.db.delete(inventario)
        self.db.commit()