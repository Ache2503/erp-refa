"""
Controllers — Proveedores & Contactos
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.proveedor_service import ProveedorService
from app.schemas.proveedores import (
    ProveedorCreate, ProveedorUpdate,
    ProveedorResponse, ProveedorConContactos, ProveedorListResponse,
    ContactoCreate, ContactoUpdate, ContactoResponse,
)

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


# ── CRUD Proveedor ───────────────────────────────────────────────

@router.get("", response_model=ProveedorListResponse, summary="Listar proveedores")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return ProveedorService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[ProveedorResponse],
            summary="Buscar proveedores por nombre o email")
def buscar(
    q: str     = Query(..., min_length=1, description="Texto a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return ProveedorService(db).buscar(q, skip, limit)


@router.post("", response_model=ProveedorResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear proveedor")
def crear(data: ProveedorCreate, db: Session = Depends(get_db)):
    return ProveedorService(db).crear(data)


@router.get("/{id_proveedor}", response_model=ProveedorConContactos,
            summary="Obtener proveedor con sus contactos")
def obtener(id_proveedor: int, db: Session = Depends(get_db)):
    return ProveedorService(db).obtener_con_contactos(id_proveedor)


@router.put("/{id_proveedor}", response_model=ProveedorResponse,
            summary="Actualizar proveedor")
def actualizar(id_proveedor: int, data: ProveedorUpdate,
               db: Session = Depends(get_db)):
    return ProveedorService(db).actualizar(id_proveedor, data)


@router.delete("/{id_proveedor}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar proveedor")
def eliminar(id_proveedor: int, db: Session = Depends(get_db)):
    ProveedorService(db).eliminar(id_proveedor)


# ── CRUD Contactos ───────────────────────────────────────────────

@router.get("/{id_proveedor}/contactos", response_model=list[ContactoResponse],
            summary="Listar contactos de un proveedor")
def listar_contactos(id_proveedor: int, db: Session = Depends(get_db)):
    return ProveedorService(db).listar_contactos(id_proveedor)


@router.post("/{id_proveedor}/contactos", response_model=ContactoResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear contacto para un proveedor")
def crear_contacto(id_proveedor: int, data: ContactoCreate,
                   db: Session = Depends(get_db)):
    return ProveedorService(db).crear_contacto(id_proveedor, data)


@router.get("/contactos/{id_contacto}", response_model=ContactoResponse,
            summary="Obtener contacto por ID")
def obtener_contacto(id_contacto: int, db: Session = Depends(get_db)):
    return ProveedorService(db).obtener_contacto(id_contacto)


@router.put("/contactos/{id_contacto}", response_model=ContactoResponse,
            summary="Actualizar contacto")
def actualizar_contacto(id_contacto: int, data: ContactoUpdate,
                        db: Session = Depends(get_db)):
    return ProveedorService(db).actualizar_contacto(id_contacto, data)


@router.delete("/contactos/{id_contacto}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar contacto")
def eliminar_contacto(id_contacto: int, db: Session = Depends(get_db)):
    ProveedorService(db).eliminar_contacto(id_contacto)