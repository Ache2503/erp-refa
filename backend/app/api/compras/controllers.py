"""
Controllers — Compras
Órdenes de compra a proveedores
"""
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.compra_service import CompraService
from app.schemas.compras import (
    CompraCreate, CompraUpdate,
    CompraResponse, CompraConDetalles, CompraConRelaciones, CompraListResponse,
    CompraDetalleResponse, CompraDetalleConProducto,
)

router = APIRouter(prefix="/compras", tags=["Compras"])


# ════════════════════════════════════════════════════════════════
# COMPRAS (ÓRDENES)
# ════════════════════════════════════════════════════════════════

@router.get("", response_model=CompraListResponse, summary="Listar compras")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CompraService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[CompraResponse],
            summary="Buscar compras por número de orden")
def buscar(
    q: str     = Query(..., min_length=1, description="Número de orden"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return CompraService(db).buscar(q, skip, limit)


@router.post("", response_model=CompraConDetalles,
             status_code=status.HTTP_201_CREATED,
             summary="Crear compra con detalles")
def crear(data: CompraCreate, db: Session = Depends(get_db)):
    return CompraService(db).crear(data)


@router.get("/{id_compra}", response_model=CompraConRelaciones,
            summary="Obtener compra con detalles y relaciones")
def obtener(id_compra: int, db: Session = Depends(get_db)):
    return CompraService(db).obtener(id_compra)


@router.put("/{id_compra}", response_model=CompraResponse,
            summary="Actualizar compra (solo campos permitidos)")
def actualizar(id_compra: int, data: CompraUpdate,
               db: Session = Depends(get_db)):
    return CompraService(db).actualizar(id_compra, data)


@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar compra (solo si está pendiente o cancelada)")
def eliminar(id_compra: int, db: Session = Depends(get_db)):
    CompraService(db).eliminar(id_compra)


@router.get("/proveedor/{id_proveedor}", response_model=list[CompraResponse],
            summary="Listar compras de un proveedor")
def listar_por_proveedor(
    id_proveedor: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CompraService(db).listar_por_proveedor(id_proveedor, skip, limit)


@router.get("/estado/{estado}", response_model=list[CompraResponse],
            summary="Listar compras por estado")
def listar_por_estado(
    estado: str = Path(..., description="pendiente/confirmada/entregada/cancelada"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CompraService(db).listar_por_estado(estado, skip, limit)


@router.get("/empleado/{id_empleado}", response_model=list[CompraResponse],
            summary="Listar compras de un empleado")
def listar_por_empleado(
    id_empleado: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CompraService(db).listar_por_empleado(id_empleado, skip, limit)


# ════════════════════════════════════════════════════════════════
# DETALLES DE COMPRA
# ════════════════════════════════════════════════════════════════

@router.get("/{id_compra}/detalles", response_model=list[CompraDetalleConProducto],
            summary="Listar detalles de una compra")
def listar_detalles(id_compra: int, db: Session = Depends(get_db)):
    return CompraService(db).listar_detalles(id_compra)


@router.get("/detalles/{id_compra_detalle}", response_model=CompraDetalleConProducto,
            summary="Obtener detalle con producto")
def obtener_detalle(id_compra_detalle: int, db: Session = Depends(get_db)):
    return CompraService(db).obtener_detalle(id_compra_detalle)


@router.delete("/detalles/{id_compra_detalle}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar detalle (solo si compra está pendiente)")
def eliminar_detalle(id_compra_detalle: int, db: Session = Depends(get_db)):
    CompraService(db).eliminar_detalle(id_compra_detalle)