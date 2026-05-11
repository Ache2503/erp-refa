"""
Service — Clientes
Lógica de negocio: validaciones de unicidad, manejo de estatus.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.cliente_repository import ClienteRepository
from app.schemas.clientes import (
    ClienteCreate, ClienteUpdate,
    ClienteResponse, ClienteListResponse,
)


class ClienteService:

    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    # ── Listado y búsqueda ────────────────────────────────────────

    def listar(self, skip: int = 0, limit: int = 100) -> ClienteListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return ClienteListResponse(
            total=total, skip=skip, limit=limit,
            data=[ClienteResponse.model_validate(c) for c in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[ClienteResponse]:
        return [
            ClienteResponse.model_validate(c)
            for c in self.repo.buscar(q, skip, limit)
        ]

    def listar_por_estatus(self, estatus: str, skip: int = 0,
                           limit: int = 100) -> list[ClienteResponse]:
        return [
            ClienteResponse.model_validate(c)
            for c in self.repo.filtrar_por_estatus(estatus, skip, limit)
        ]

    # ── CRUD ──────────────────────────────────────────────────────

    def obtener(self, id_cliente: int) -> ClienteResponse:
        cliente = self.repo.get_by_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no encontrado",
            )
        return ClienteResponse.model_validate(cliente)

    def crear(self, data: ClienteCreate) -> ClienteResponse:
        # Email único (si se provee)
        if data.email and self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un cliente con el email '{data.email}'",
            )
        # RFC único (si se provee)
        if data.rfc and self.repo.get_by_rfc(data.rfc):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un cliente con el RFC '{data.rfc}'",
            )
        return ClienteResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_cliente: int,
                   data: ClienteUpdate) -> ClienteResponse:
        cliente = self.repo.get_by_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no encontrado",
            )
        # Validar unicidad solo si cambia el valor
        if data.email and data.email != cliente.email:
            if self.repo.get_by_email(data.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El email '{data.email}' ya está en uso",
                )
        if data.rfc and data.rfc != cliente.rfc:
            if self.repo.get_by_rfc(data.rfc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El RFC '{data.rfc}' ya está en uso",
                )
        return ClienteResponse.model_validate(self.repo.update(cliente, data))

    def eliminar(self, id_cliente: int) -> None:
        cliente = self.repo.get_by_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no encontrado",
            )
        self.repo.delete(cliente)

    # ── Estatus ───────────────────────────────────────────────────

    def activar(self, id_cliente: int) -> ClienteResponse:
        cliente = self.repo.get_by_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no encontrado",
            )
        if cliente.estatus == "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente ya está activo",
            )
        return ClienteResponse.model_validate(
            self.repo.cambiar_estatus(cliente, "activo")
        )

    def desactivar(self, id_cliente: int) -> ClienteResponse:
        cliente = self.repo.get_by_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente {id_cliente} no encontrado",
            )
        if cliente.estatus == "inactivo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente ya está inactivo",
            )
        return ClienteResponse.model_validate(
            self.repo.cambiar_estatus(cliente, "inactivo")
        )