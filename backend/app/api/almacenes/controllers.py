"""
Controllers — Almacenes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.almacen_service import AlmacenService
from app.schemas.almacenes import (
    AlmacenCreate, AlmacenUpdate,
    AlmacenResponse, AlmacenConRelaciones, AlmacenListResponse,
)

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])


@router.get("", response_model=AlmacenListResponse, summary="Listar almacenes")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return AlmacenService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[AlmacenResponse],
            summary="Buscar almacenes por nombre o ubicación")
def buscar(
    q: str     = Query(..., min_length=1, description="Texto a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return AlmacenService(db).buscar(q, skip, limit)


@router.post("", response_model=AlmacenResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear almacén")
def crear(data: AlmacenCreate, db: Session = Depends(get_db)):
    return AlmacenService(db).crear(data)


@router.get("/{id_almacen}", response_model=AlmacenConRelaciones,
            summary="Obtener almacén con relaciones")
def obtener(id_almacen: int, db: Session = Depends(get_db)):
    return AlmacenService(db).obtener(id_almacen)


@router.put("/{id_almacen}", response_model=AlmacenResponse,
            summary="Actualizar almacén")
def actualizar(id_almacen: int, data: AlmacenUpdate,
               db: Session = Depends(get_db)):
    return AlmacenService(db).actualizar(id_almacen, data)


@router.delete("/{id_almacen}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar almacén")
def eliminar(id_almacen: int, db: Session = Depends(get_db)):
    AlmacenService(db).eliminar(id_almacen)


@router.get("/empleado/{id_empleado}", response_model=list[AlmacenResponse],
            summary="Listar almacenes de un empleado")
def listar_por_empleado(
    id_empleado: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return AlmacenService(db).listar_por_empleado(id_empleado, skip, limit)


@router.get("/tipo/{id_tipo_almacen}", response_model=list[AlmacenResponse],
            summary="Listar almacenes por tipo")
def listar_por_tipo(
    id_tipo_almacen: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return AlmacenService(db).listar_por_tipo(id_tipo_almacen, skip, limit)