"""
Service — Roles & Permisos
Lógica de negocio: validaciones, reglas, orquestación.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.rol_repository import RolRepository
from app.schemas.roles import (
    RolCreate, RolUpdate, RolResponse, RolConPermisos,
    PermisoCreate, PermisoUpdate, PermisoResponse,
    AsignarPermisoRequest, EmpleadoRolResponse,
)


class RolService:

    def __init__(self, db: Session):
        self.repo = RolRepository(db)

    # ── Roles ─────────────────────────────────────────────────────

    def listar_roles(self, skip: int = 0, limit: int = 100) -> list[RolResponse]:
        return [RolResponse.model_validate(r) for r in self.repo.get_all(skip, limit)]

    def obtener_rol(self, id_rol: int) -> RolResponse:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        return RolResponse.model_validate(rol)

    def obtener_rol_con_permisos(self, id_rol: int) -> RolConPermisos:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        permisos = self.repo.get_permisos_de_rol(id_rol)
        data = RolConPermisos.model_validate(rol)
        data.permisos = [PermisoResponse.model_validate(p) for p in permisos]
        return data

    def crear_rol(self, data: RolCreate) -> RolResponse:
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Ya existe un rol con nombre '{data.nombre}'")
        return RolResponse.model_validate(self.repo.create(data))

    def actualizar_rol(self, id_rol: int, data: RolUpdate) -> RolResponse:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        if data.nombre and data.nombre != rol.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Ya existe un rol con nombre '{data.nombre}'")
        return RolResponse.model_validate(self.repo.update(rol, data))

    def eliminar_rol(self, id_rol: int) -> None:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        self.repo.delete(rol)

    # ── Permisos ──────────────────────────────────────────────────

    def listar_permisos(self, skip: int = 0, limit: int = 100) -> list[PermisoResponse]:
        return [PermisoResponse.model_validate(p) for p in self.repo.get_all_permisos(skip, limit)]

    def obtener_permiso(self, id_permiso: int) -> PermisoResponse:
        p = self.repo.get_permiso_by_id(id_permiso)
        if not p:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Permiso {id_permiso} no encontrado")
        return PermisoResponse.model_validate(p)

    def crear_permiso(self, data: PermisoCreate) -> PermisoResponse:
        if self.repo.get_permiso_by_nombre(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Ya existe un permiso con nombre '{data.nombre}'")
        return PermisoResponse.model_validate(self.repo.create_permiso(data))

    def actualizar_permiso(self, id_permiso: int, data: PermisoUpdate) -> PermisoResponse:
        p = self.repo.get_permiso_by_id(id_permiso)
        if not p:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Permiso {id_permiso} no encontrado")
        if data.nombre and data.nombre != p.nombre:
            if self.repo.get_permiso_by_nombre(data.nombre):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Ya existe un permiso con nombre '{data.nombre}'")
        return PermisoResponse.model_validate(self.repo.update_permiso(p, data))

    def eliminar_permiso(self, id_permiso: int) -> None:
        p = self.repo.get_permiso_by_id(id_permiso)
        if not p:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Permiso {id_permiso} no encontrado")
        self.repo.delete_permiso(p)

    # ── Asignación Rol-Permiso ────────────────────────────────────

    def asignar_permisos_a_rol(self, id_rol: int, data: AsignarPermisoRequest) -> RolConPermisos:
        rol = self.repo.get_by_id(id_rol)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        for id_permiso in data.id_permisos:
            if not self.repo.get_permiso_by_id(id_permiso):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Permiso {id_permiso} no encontrado")
            if not self.repo.permiso_ya_asignado(id_rol, id_permiso):
                self.repo.asignar_permiso(id_rol, id_permiso)
        return self.obtener_rol_con_permisos(id_rol)

    def quitar_permiso_de_rol(self, id_rol: int, id_permiso: int) -> RolConPermisos:
        if not self.repo.get_by_id(id_rol):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        eliminado = self.repo.quitar_permiso(id_rol, id_permiso)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"El permiso {id_permiso} no estaba asignado a este rol")
        return self.obtener_rol_con_permisos(id_rol)

    # ── Asignación Empleado-Rol ───────────────────────────────────

    def asignar_rol_a_empleado(self, id_empleado: int, id_rol: int) -> EmpleadoRolResponse:
        if not self.repo.get_by_id(id_rol):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rol {id_rol} no encontrado")
        if self.repo.rol_ya_asignado(id_empleado, id_rol):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El empleado ya tiene ese rol asignado")
        er = self.repo.asignar_rol_a_empleado(id_empleado, id_rol)
        return EmpleadoRolResponse.model_validate(er)

    def quitar_rol_de_empleado(self, id_empleado: int, id_rol: int) -> None:
        eliminado = self.repo.quitar_rol_de_empleado(id_empleado, id_rol)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El empleado no tiene ese rol asignado")

    def listar_roles_de_empleado(self, id_empleado: int) -> list[EmpleadoRolResponse]:
        ers = self.repo.get_roles_de_empleado(id_empleado)
        return [EmpleadoRolResponse.model_validate(er) for er in ers]