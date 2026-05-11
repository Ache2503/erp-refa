"""
Controllers — Vehículos
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.vehiculo_service import VehiculoService
from app.schemas.vehiculos import (
    VehiculoCreate, VehiculoUpdate,
    VehiculoResponse, VehiculoConRelaciones, VehiculoListResponse,
)

router = APIRouter(prefix="/vehiculos", tags=["Transporte"])


@router.get("", response_model=VehiculoListResponse, summary="Listar vehículos")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VehiculoService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[VehiculoResponse],
            summary="Buscar vehículos por placa")
def buscar(
    q: str     = Query(..., min_length=1, description="Placa a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return VehiculoService(db).buscar(q, skip, limit)


@router.post("", response_model=VehiculoResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear vehículo")
def crear(data: VehiculoCreate, db: Session = Depends(get_db)):
    return VehiculoService(db).crear(data)


@router.get("/{id_vehiculo}", response_model=VehiculoConRelaciones,
            summary="Obtener vehículo con relaciones")
def obtener(id_vehiculo: int, db: Session = Depends(get_db)):
    return VehiculoService(db).obtener(id_vehiculo)


@router.put("/{id_vehiculo}", response_model=VehiculoResponse,
            summary="Actualizar vehículo")
def actualizar(id_vehiculo: int, data: VehiculoUpdate,
               db: Session = Depends(get_db)):
    return VehiculoService(db).actualizar(id_vehiculo, data)


@router.delete("/{id_vehiculo}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar vehículo")
def eliminar(id_vehiculo: int, db: Session = Depends(get_db)):
    VehiculoService(db).eliminar(id_vehiculo)


@router.get("/conductor/{id_conductor}", response_model=list[VehiculoResponse],
            summary="Listar vehículos de un conductor")
def listar_por_conductor(
    id_conductor: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VehiculoService(db).listar_por_conductor(id_conductor, skip, limit)


@router.get("/tipo/{id_tipo_vehiculo}", response_model=list[VehiculoResponse],
            summary="Listar vehículos por tipo")
def listar_por_tipo(
    id_tipo_vehiculo: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VehiculoService(db).listar_por_tipo(id_tipo_vehiculo, skip, limit)


@router.get("/estado/{estado}", response_model=list[VehiculoResponse],
            summary="Listar vehículos por estado (activo/inactivo/mantenimiento)")
def listar_por_estado(
    estado: str,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VehiculoService(db).listar_por_estado(estado, skip, limit)