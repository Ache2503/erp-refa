"""
Controllers — Tipos de Almacén
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.tipos_almacen_service import TipoAlmacenService
from app.schemas.tipos_almacen import (
    TipoAlmacenCreate, TipoAlmacenUpdate,
    TipoAlmacenResponse, TipoAlmacenListResponse,
)

router = APIRouter(prefix="/tipos-almacen", tags=["Almacenes"])


@router.get("", response_model=TipoAlmacenListResponse,
            summary="Listar tipos de almacén")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return TipoAlmacenService(db).listar(skip, limit)


@router.post("", response_model=TipoAlmacenResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear tipo de almacén")
def crear(data: TipoAlmacenCreate, db: Session = Depends(get_db)):
    return TipoAlmacenService(db).crear(data)


@router.get("/{id_tipo_almacen}", response_model=TipoAlmacenResponse,
            summary="Obtener tipo de almacén")
def obtener(id_tipo_almacen: int, db: Session = Depends(get_db)):
    return TipoAlmacenService(db).obtener(id_tipo_almacen)


@router.put("/{id_tipo_almacen}", response_model=TipoAlmacenResponse,
            summary="Actualizar tipo de almacén")
def actualizar(id_tipo_almacen: int, data: TipoAlmacenUpdate,
               db: Session = Depends(get_db)):
    return TipoAlmacenService(db).actualizar(id_tipo_almacen, data)


@router.delete("/{id_tipo_almacen}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar tipo de almacén")
def eliminar(id_tipo_almacen: int, db: Session = Depends(get_db)):
    TipoAlmacenService(db).eliminar(id_tipo_almacen)