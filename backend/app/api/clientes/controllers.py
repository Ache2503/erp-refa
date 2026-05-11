"""
Controllers — Clientes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.cliente_service import ClienteService
from app.schemas.clientes import (
    ClienteCreate, ClienteUpdate,
    ClienteResponse, ClienteListResponse,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


# ── CRUD ──────────────────────────────────────────────────────────

@router.get("", response_model=ClienteListResponse, summary="Listar clientes")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return ClienteService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[ClienteResponse],
            summary="Buscar clientes por nombre, apellido o email")
def buscar(
    q: str     = Query(..., min_length=1, description="Texto a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return ClienteService(db).buscar(q, skip, limit)


@router.get("/estatus/{estatus}", response_model=list[ClienteResponse],
            summary="Filtrar por estatus (activo | inactivo)")
def por_estatus(
    estatus: str,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return ClienteService(db).listar_por_estatus(estatus, skip, limit)


@router.post("", response_model=ClienteResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear cliente")
def crear(data: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService(db).crear(data)


@router.get("/{id_cliente}", response_model=ClienteResponse,
            summary="Obtener cliente por ID")
def obtener(id_cliente: int, db: Session = Depends(get_db)):
    return ClienteService(db).obtener(id_cliente)


@router.put("/{id_cliente}", response_model=ClienteResponse,
            summary="Actualizar cliente")
def actualizar(id_cliente: int, data: ClienteUpdate,
               db: Session = Depends(get_db)):
    return ClienteService(db).actualizar(id_cliente, data)


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar cliente")
def eliminar(id_cliente: int, db: Session = Depends(get_db)):
    ClienteService(db).eliminar(id_cliente)


# ── Estatus rápido ────────────────────────────────────────────────

@router.patch("/{id_cliente}/activar", response_model=ClienteResponse,
              summary="Activar cliente")
def activar(id_cliente: int, db: Session = Depends(get_db)):
    return ClienteService(db).activar(id_cliente)


@router.patch("/{id_cliente}/desactivar", response_model=ClienteResponse,
              summary="Desactivar cliente")
def desactivar(id_cliente: int, db: Session = Depends(get_db)):
    return ClienteService(db).desactivar(id_cliente)