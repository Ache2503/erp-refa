"""
Controllers — Logística
Gestión de envíos
"""
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.logistica_service import LogisticaService
from app.schemas.logistica import (
    EnvioCreate, EnvioUpdate,
    EnvioResponse, EnvioConDetalles, EnvioListResponse,
)

router = APIRouter(prefix="/logistica", tags=["Logística"])


# ════════════════════════════════════════════════════════════════
# ENVÍOS
# ════════════════════════════════════════════════════════════════

@router.get("", response_model=EnvioListResponse, summary="Listar envíos")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return LogisticaService(db).listar(skip, limit)


@router.post("", response_model=EnvioResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear envío")
def crear(data: EnvioCreate, db: Session = Depends(get_db)):
    return LogisticaService(db).crear(data)


@router.get("/{id_envio}", response_model=EnvioConDetalles,
            summary="Obtener envío")
def obtener(id_envio: int, db: Session = Depends(get_db)):
    return LogisticaService(db).obtener(id_envio)


@router.put("/{id_envio}", response_model=EnvioResponse,
            summary="Actualizar envío")
def actualizar(id_envio: int, data: EnvioUpdate,
               db: Session = Depends(get_db)):
    return LogisticaService(db).actualizar(id_envio, data)


@router.delete("/{id_envio}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar envío")
def eliminar(id_envio: int, db: Session = Depends(get_db)):
    LogisticaService(db).eliminar(id_envio)


@router.get("/estado/{estado}", response_model=list[EnvioResponse],
            summary="Listar envíos por estado")
def listar_por_estado(
    estado: str = Path(..., description="pendiente/en_transito/entregado"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return LogisticaService(db).listar_por_estado(estado, skip, limit)


@router.get("/vehiculo/{id_vehiculo}", response_model=list[EnvioResponse],
            summary="Listar envíos de un vehículo")
def listar_por_vehiculo(
    id_vehiculo: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return LogisticaService(db).listar_por_vehiculo(id_vehiculo, skip, limit)


@router.get("/empleado/{id_empleado}", response_model=list[EnvioResponse],
            summary="Listar envíos de un empleado")
def listar_por_empleado(
    id_empleado: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return LogisticaService(db).listar_por_empleado(id_empleado, skip, limit)