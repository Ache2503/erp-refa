"""
Service — Empleados
Lógica de negocio: validaciones de unicidad, reglas de estatus.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.empleados import (
    EmpleadoCreate, EmpleadoUpdate,
    EmpleadoResponse, EmpleadoListResponse,
)


class EmpleadoService:

    def __init__(self, db: Session):
        self.repo = EmpleadoRepository(db)

    # ── Listado y búsqueda ────────────────────────────────────────

    def listar(self, skip: int = 0, limit: int = 100) -> EmpleadoListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return EmpleadoListResponse(
            total = total, skip=skip, limit=limit,
            data=[EmpleadoResponse.model_validate(e) for e in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[EmpleadoResponse]:
        return [
            EmpleadoResponse.model_validate(e)
            for e in self.repo.buscar(q, skip, limit)
        ]

    def listar_por_estatus(self, estatus: str, skip: int = 0,
                           limit: int = 100) -> list[EmpleadoResponse]:
        return [
            EmpleadoResponse.model_validate(e)
            for e in self.repo.filtrar_por_estatus(estatus, skip, limit)
        ]

    # ── CRUD ──────────────────────────────────────────────────────

    def obtener(self, id_empleado: int) -> EmpleadoResponse:
        emp = self.repo.get_by_id(id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        return EmpleadoResponse.model_validate(emp)

    def crear(self, data: EmpleadoCreate) -> EmpleadoResponse:
        # Email único
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un empleado con el email '{data.email}'",
            )
        # RFC único (si se provee)
        if data.rfc and self.repo.get_by_rfc(data.rfc):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un empleado con el RFC '{data.rfc}'",
            )
        # NSS único (si se provee)
        if data.numero_seguridad_social and self.repo.get_by_nss(data.numero_seguridad_social):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un empleado con ese número de seguridad social",
            )
        return EmpleadoResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_empleado: int,
                   data: EmpleadoUpdate) -> EmpleadoResponse:
        emp = self.repo.get_by_id(id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        # Validar unicidad solo si cambia el valor
        if data.email and data.email != emp.email:
            if self.repo.get_by_email(data.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El email '{data.email}' ya está en uso",
                )
        if data.rfc and data.rfc != emp.rfc:
            if self.repo.get_by_rfc(data.rfc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El RFC '{data.rfc}' ya está en uso",
                )
        if data.numero_seguridad_social and data.numero_seguridad_social != emp.numero_seguridad_social:
            if self.repo.get_by_nss(data.numero_seguridad_social):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El número de seguridad social ya está en uso",
                )
        return EmpleadoResponse.model_validate(self.repo.update(emp, data))

    def eliminar(self, id_empleado: int) -> None:
        emp = self.repo.get_by_id(id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        self.repo.delete(emp)

    # ── Estatus ───────────────────────────────────────────────────

    def activar(self, id_empleado: int) -> EmpleadoResponse:
        emp = self.repo.get_by_id(id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        if emp.estatus == "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El empleado ya está activo",
            )
        return EmpleadoResponse.model_validate(
            self.repo.cambiar_estatus(emp, "activo")
        )

    def desactivar(self, id_empleado: int) -> EmpleadoResponse:
        emp = self.repo.get_by_id(id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        if emp.estatus == "inactivo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El empleado ya está inactivo",
            )
        return EmpleadoResponse.model_validate(
            self.repo.cambiar_estatus(emp, "inactivo")
        )