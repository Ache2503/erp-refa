"""
Controllers — Ventas
Venta directa a clientes
"""
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.venta_service import VentaService
from app.services.venta_completa_service import VentaCompletaService
from app.schemas.ventas import (
    VentaCreate, VentaUpdate,
    VentaResponse, VentaConDetalles, VentaListResponse,
)
from app.schemas.venta_completa import VentaCompletaRequest, VentaCompletaResponse

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("", response_model=VentaListResponse, summary="Listar ventas")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VentaService(db).listar(skip, limit)


@router.post("", response_model=VentaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear venta")
def crear(data: VentaCreate, db: Session = Depends(get_db)):
    return VentaService(db).crear(data)


@router.get("/{id_venta}", response_model=VentaConDetalles,
            summary="Obtener venta")
def obtener(id_venta: int, db: Session = Depends(get_db)):
    return VentaService(db).obtener(id_venta)


@router.put("/{id_venta}", response_model=VentaResponse,
            summary="Actualizar venta")
def actualizar(id_venta: int, data: VentaUpdate,
               db: Session = Depends(get_db)):
    return VentaService(db).actualizar(id_venta, data)


@router.delete("/{id_venta}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar venta")
def eliminar(id_venta: int, db: Session = Depends(get_db)):
    VentaService(db).eliminar(id_venta)


@router.get("/cliente/{id_cliente}", response_model=list[VentaResponse],
            summary="Listar ventas de un cliente")
def listar_por_cliente(
    id_cliente: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return VentaService(db).listar_por_cliente(id_cliente, skip, limit)


@router.post("/completa", response_model=VentaCompletaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Venta completa con detalles, envío y guía")
def venta_completa(data: VentaCompletaRequest, db: Session = Depends(get_db)):
    return VentaCompletaService(db).ejecutar(data)


@router.get("/{id_venta}/ticket", summary="Generar ticket de venta")
def ticket(id_venta: int, db: Session = Depends(get_db)):
    return VentaCompletaService(db).ticket(id_venta)