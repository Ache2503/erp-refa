"""
Controllers — Unidades de Medida
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.unidad_medida_service import UnidadMedidaService
from app.schemas.unidades_medida import (
    UnidadMedidaCreate, UnidadMedidaUpdate,
    UnidadMedidaResponse, UnidadMedidaListResponse,
)

router = APIRouter(prefix="/unidades-medida", tags=["Unidades de Medida"])


@router.get("", response_model=UnidadMedidaListResponse,
            summary="Listar unidades de medida")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return UnidadMedidaService(db).listar(skip, limit)


@router.post("", response_model=UnidadMedidaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear unidad de medida")
def crear(data: UnidadMedidaCreate, db: Session = Depends(get_db)):
    return UnidadMedidaService(db).crear(data)


@router.get("/{id_unidad_medida}", response_model=UnidadMedidaResponse,
            summary="Obtener unidad de medida")
def obtener(id_unidad_medida: int, db: Session = Depends(get_db)):
    return UnidadMedidaService(db).obtener(id_unidad_medida)


@router.put("/{id_unidad_medida}", response_model=UnidadMedidaResponse,
            summary="Actualizar unidad de medida")
def actualizar(id_unidad_medida: int, data: UnidadMedidaUpdate,
               db: Session = Depends(get_db)):
    return UnidadMedidaService(db).actualizar(id_unidad_medida, data)


@router.delete("/{id_unidad_medida}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar unidad de medida")
def eliminar(id_unidad_medida: int, db: Session = Depends(get_db)):
    UnidadMedidaService(db).eliminar(id_unidad_medida)