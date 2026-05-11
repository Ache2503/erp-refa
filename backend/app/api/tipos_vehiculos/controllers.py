"""
Controllers - tipos_vehiculos
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.tipo_vehiculo_service import TipoVehiculoService
from app.schemas.tipos_vehiculos import (
    TipoVehiculoCreate, TipoVehiculoUpdate,
    TipoVehiculoResponse, TipoVehiculoListResponse,
)

router = APIRouter(prefix="/tipos-vehiculos", tags=["Transporte"])

@router.get("", response_model=TipoVehiculoListResponse, summary="Listar tipos de vehículos")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return TipoVehiculoService(db).listar(skip, limit)


@router.post("", response_model=TipoVehiculoResponse,
          status_code=status.HTTP_201_CREATED, summary="Crear tipo de vehículo")
def crear(data: TipoVehiculoCreate, db: Session = Depends(get_db)):
    return TipoVehiculoService(db).crear(data)
