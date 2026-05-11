"""
Service — Proveedores & Contactos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.proveedor_repository import ProveedorRepository
from app.schemas.proveedores import (
    ProveedorCreate, ProveedorUpdate,
    ProveedorResponse, ProveedorConContactos, ProveedorListResponse,
    ContactoCreate, ContactoUpdate, ContactoResponse,
)


class ProveedorService:

    def __init__(self, db: Session):
        self.repo = ProveedorRepository(db)

    # ── Listado y búsqueda ────────────────────────────────────────

    def listar(self, skip: int = 0, limit: int = 100) -> ProveedorListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return ProveedorListResponse(
            total=total, skip=skip, limit=limit,
            data=[ProveedorResponse.model_validate(p) for p in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[ProveedorResponse]:
        return [
            ProveedorResponse.model_validate(p)
            for p in self.repo.buscar(q, skip, limit)
        ]

    # ── CRUD Proveedor ────────────────────────────────────────────

    def obtener(self, id_proveedor: int) -> ProveedorResponse:
        p = self.repo.get_by_id(id_proveedor)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        return ProveedorResponse.model_validate(p)

    def obtener_con_contactos(self, id_proveedor: int) -> ProveedorConContactos:
        p = self.repo.get_by_id(id_proveedor)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        contactos = self.repo.get_contactos(id_proveedor)
        data = ProveedorConContactos.model_validate(p)
        data.contactos = [ContactoResponse.model_validate(c) for c in contactos]
        return data

    def crear(self, data: ProveedorCreate) -> ProveedorResponse:
        return ProveedorResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_proveedor: int,
                   data: ProveedorUpdate) -> ProveedorResponse:
        p = self.repo.get_by_id(id_proveedor)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        return ProveedorResponse.model_validate(self.repo.update(p, data))

    def eliminar(self, id_proveedor: int) -> None:
        p = self.repo.get_by_id(id_proveedor)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        self.repo.delete(p)

    # ── CRUD Contactos ────────────────────────────────────────────

    def listar_contactos(self, id_proveedor: int) -> list[ContactoResponse]:
        if not self.repo.get_by_id(id_proveedor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        contactos = self.repo.get_contactos(id_proveedor)
        return [ContactoResponse.model_validate(c) for c in contactos]

    def obtener_contacto(self, id_contacto: int) -> ContactoResponse:
        c = self.repo.get_contacto_by_id(id_contacto)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contacto {id_contacto} no encontrado",
            )
        return ContactoResponse.model_validate(c)

    def crear_contacto(self, id_proveedor: int,
                       data: ContactoCreate) -> ContactoResponse:
        if not self.repo.get_by_id(id_proveedor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no encontrado",
            )
        return ContactoResponse.model_validate(
            self.repo.create_contacto(id_proveedor, data)
        )

    def actualizar_contacto(self, id_contacto: int,
                            data: ContactoUpdate) -> ContactoResponse:
        c = self.repo.get_contacto_by_id(id_contacto)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contacto {id_contacto} no encontrado",
            )
        return ContactoResponse.model_validate(self.repo.update_contacto(c, data))

    def eliminar_contacto(self, id_contacto: int) -> None:
        c = self.repo.get_contacto_by_id(id_contacto)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contacto {id_contacto} no encontrado",
            )
        self.repo.delete_contacto(c)