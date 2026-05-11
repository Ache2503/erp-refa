"""
Controllers — Inventario
Gestión de inventario/stock
"""
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.inventario_service import InventarioService
from app.schemas.inventario import (
    InventarioCreate, InventarioUpdate, InventarioAjuste,
    InventarioResponse, InventarioListResponse,
)

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("", response_model=InventarioListResponse, summary="Listar inventario")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return InventarioService(db).listar(skip, limit)


@router.post("", response_model=InventarioResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear registro de inventario")
def crear(data: InventarioCreate, db: Session = Depends(get_db)):
    return InventarioService(db).crear(data)


@router.get("/bajo-stock", response_model=list[InventarioResponse],
            summary="Productos con stock bajo mínimo")
def bajo_stock(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return InventarioService(db).bajo_stock(skip, limit)


@router.get("/producto/{id_producto}", response_model=list[InventarioResponse],
            summary="Inventario de un producto")
def listar_por_producto(
    id_producto: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return InventarioService(db).listar_por_producto(id_producto, skip, limit)


@router.get("/almacen/{id_almacen}", response_model=list[InventarioResponse],
            summary="Inventario de un almacén")
def listar_por_almacen(
    id_almacen: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return InventarioService(db).listar_por_almacen(id_almacen, skip, limit)


@router.get("/{id_inventario}", response_model=InventarioResponse,
            summary="Obtener registro de inventario")
def obtener(id_inventario: int, db: Session = Depends(get_db)):
    return InventarioService(db).obtener(id_inventario)


@router.put("/{id_inventario}", response_model=InventarioResponse,
            summary="Actualizar inventario")
def actualizar(id_inventario: int, data: InventarioUpdate,
               db: Session = Depends(get_db)):
    return InventarioService(db).actualizar(id_inventario, data)


@router.post("/{id_inventario}/ajustar", response_model=InventarioResponse,
            summary="Ajustar stock")
def ajustar(id_inventario: int, data: InventarioAjuste,
            db: Session = Depends(get_db)):
    return InventarioService(db).ajustar(id_inventario, data)


@router.delete("/{id_inventario}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar registro de inventario")
def eliminar(id_inventario: int, db: Session = Depends(get_db)):
    InventarioService(db).eliminar(id_inventario)