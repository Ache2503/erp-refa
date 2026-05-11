"""
Controllers — Roles & Permisos
Endpoints REST organizados por recurso.
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.rol_service import RolService
from app.schemas.roles import (
    RolCreate, RolUpdate, RolResponse, RolConPermisos,
    PermisoCreate, PermisoUpdate, PermisoResponse,
    AsignarPermisoRequest, AsignarRolRequest, EmpleadoRolResponse,
)

router = APIRouter(tags=["Roles & Permisos"])


# ════════════════════════════════════════════════════════════════
# ROLES
# ════════════════════════════════════════════════════════════════

@router.get("/roles", response_model=list[RolResponse], summary="Listar roles")
def listar_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return RolService(db).listar_roles(skip, limit)


@router.post("/roles", response_model=RolResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear rol")
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return RolService(db).crear_rol(data)


@router.get("/roles/{id_rol}", response_model=RolConPermisos,
            summary="Obtener rol con sus permisos")
def obtener_rol(id_rol: int, db: Session = Depends(get_db)):
    return RolService(db).obtener_rol_con_permisos(id_rol)


@router.put("/roles/{id_rol}", response_model=RolResponse, summary="Actualizar rol")
def actualizar_rol(id_rol: int, data: RolUpdate, db: Session = Depends(get_db)):
    return RolService(db).actualizar_rol(id_rol, data)


@router.delete("/roles/{id_rol}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar rol")
def eliminar_rol(id_rol: int, db: Session = Depends(get_db)):
    RolService(db).eliminar_rol(id_rol)


# ── Permisos de un rol ────────────────────────────────────────────

@router.post("/roles/{id_rol}/permisos", response_model=RolConPermisos,
             summary="Asignar permisos a un rol")
def asignar_permisos(id_rol: int, data: AsignarPermisoRequest,
                     db: Session = Depends(get_db)):
    return RolService(db).asignar_permisos_a_rol(id_rol, data)


@router.delete("/roles/{id_rol}/permisos/{id_permiso}",
               response_model=RolConPermisos,
               summary="Quitar un permiso de un rol")
def quitar_permiso(id_rol: int, id_permiso: int, db: Session = Depends(get_db)):
    return RolService(db).quitar_permiso_de_rol(id_rol, id_permiso)


# ════════════════════════════════════════════════════════════════
# PERMISOS
# ════════════════════════════════════════════════════════════════

@router.get("/permisos", response_model=list[PermisoResponse], summary="Listar permisos")
def listar_permisos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return RolService(db).listar_permisos(skip, limit)


@router.post("/permisos", response_model=PermisoResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear permiso")
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    return RolService(db).crear_permiso(data)


@router.get("/permisos/{id_permiso}", response_model=PermisoResponse,
            summary="Obtener permiso")
def obtener_permiso(id_permiso: int, db: Session = Depends(get_db)):
    return RolService(db).obtener_permiso(id_permiso)


@router.put("/permisos/{id_permiso}", response_model=PermisoResponse,
            summary="Actualizar permiso")
def actualizar_permiso(id_permiso: int, data: PermisoUpdate,
                       db: Session = Depends(get_db)):
    return RolService(db).actualizar_permiso(id_permiso, data)


@router.delete("/permisos/{id_permiso}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar permiso")
def eliminar_permiso(id_permiso: int, db: Session = Depends(get_db)):
    RolService(db).eliminar_permiso(id_permiso)


# ════════════════════════════════════════════════════════════════
# EMPLEADO ↔ ROL
# ════════════════════════════════════════════════════════════════

@router.get("/empleados/{id_empleado}/roles",
            response_model=list[EmpleadoRolResponse],
            summary="Ver roles de un empleado")
def roles_de_empleado(id_empleado: int, db: Session = Depends(get_db)):
    return RolService(db).listar_roles_de_empleado(id_empleado)


@router.post("/empleados/{id_empleado}/roles",
             response_model=EmpleadoRolResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Asignar rol a empleado")
def asignar_rol_empleado(id_empleado: int, data: AsignarRolRequest,
                         db: Session = Depends(get_db)):
    return RolService(db).asignar_rol_a_empleado(id_empleado, data.id_rol)


@router.delete("/empleados/{id_empleado}/roles/{id_rol}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Quitar rol de empleado")
def quitar_rol_empleado(id_empleado: int, id_rol: int,
                        db: Session = Depends(get_db)):
    RolService(db).quitar_rol_de_empleado(id_empleado, id_rol)