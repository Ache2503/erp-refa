"""
Service — Inventario
Gestiona stock de productos en almacenes
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.inventario_repository import InventarioRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.almacen_repository import AlmacenRepository
from app.schemas.inventario import (
    InventarioCreate, InventarioUpdate, InventarioAjuste,
    InventarioResponse, InventarioListResponse,
)


class InventarioService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = InventarioRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.almacen_repo = AlmacenRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> InventarioListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return InventarioListResponse(
            total=total, skip=skip, limit=limit,
            data=[InventarioResponse.model_validate(i) for i in data],
        )

    def obtener(self, id: int) -> InventarioResponse:
        inv = self.repo.get_by_id(id)
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventario {id} no encontrado",
            )
        return InventarioResponse.model_validate(inv)

    def crear(self, data: InventarioCreate) -> InventarioResponse:
        if not self.producto_repo.get_by_id(data.id_producto):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {data.id_producto} no existe",
            )
        if not self.almacen_repo.get_by_id(data.id_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {data.id_almacen} no existe",
            )
        if self.repo.get_by_producto_almacen(data.id_producto, data.id_almacen):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe inventario para este producto en este almacén",
            )
        return InventarioResponse.model_validate(
            self.repo.create(
                data.id_producto, data.id_almacen,
                data.stock, data.stock_minimo, data.stock_maximo
            )
        )

    def actualizar(self, id: int, data: InventarioUpdate) -> InventarioResponse:
        inv = self.repo.get_by_id(id)
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventario {id} no encontrado",
            )
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(inv, field, value)
        self.db.commit()
        self.db.refresh(inv)
        return InventarioResponse.model_validate(inv)

    def ajustar(self, id: int, data: InventarioAjuste) -> InventarioResponse:
        inv = self.repo.get_by_id(id)
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventario {id} no encontrado",
            )
        return InventarioResponse.model_validate(
            self.repo.ajustar_stock(inv, data.cantidad)
        )

    def eliminar(self, id: int) -> None:
        inv = self.repo.get_by_id(id)
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventario {id} no encontrado",
            )
        self.repo.delete(inv)

    def listar_por_producto(self, id_producto: int, 
                           skip: int = 0, limit: int = 100) -> list[InventarioResponse]:
        if not self.producto_repo.get_by_id(id_producto):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto {id_producto} no existe",
            )
        return [
            InventarioResponse.model_validate(i)
            for i in self.repo.get_by_producto(id_producto, skip, limit)
        ]

    def listar_por_almacen(self, id_almacen: int,
                          skip: int = 0, limit: int = 100) -> list[InventarioResponse]:
        if not self.almacen_repo.get_by_id(id_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {id_almacen} no existe",
            )
        return [
            InventarioResponse.model_validate(i)
            for i in self.repo.get_by_almacen(id_almacen, skip, limit)
        ]

    def bajo_stock(self, skip: int = 0, 
                   limit: int = 100) -> list[InventarioResponse]:
        return [
            InventarioResponse.model_validate(i)
            for i in self.repo.get_bajo_stock(skip, limit)
        ]