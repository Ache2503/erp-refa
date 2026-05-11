"""
Controllers — Empleados
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.empleado_service import EmpleadoService
from app.services.rol_service import RolService
from app.schemas.empleados import (
    EmpleadoCreate, EmpleadoUpdate,
    EmpleadoResponse, EmpleadoListResponse,
)
from app.schemas.roles import EmpleadoRolResponse, AsignarRolRequest

router = APIRouter(prefix="/empleados", tags=["Empleados"])


# ── CRUD ──────────────────────────────────────────────────────────

@router.get("", response_model=EmpleadoListResponse, summary="Listar empleados")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return EmpleadoService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[EmpleadoResponse],
            summary="Buscar empleados por nombre, apellido, email o cargo")
def buscar(
    q: str     = Query(..., min_length=1, description="Texto a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return EmpleadoService(db).buscar(q, skip, limit)


@router.get("/estatus/{estatus}", response_model=list[EmpleadoResponse],
            summary="Filtrar por estatus (activo | inactivo)")
def por_estatus(
    estatus: str,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return EmpleadoService(db).listar_por_estatus(estatus, skip, limit)


@router.post("", response_model=EmpleadoResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear empleado")
def crear(data: EmpleadoCreate, db: Session = Depends(get_db)):
    return EmpleadoService(db).crear(data)


@router.get("/{id_empleado}", response_model=EmpleadoResponse,
            summary="Obtener empleado por ID")
def obtener(id_empleado: int, db: Session = Depends(get_db)):
    return EmpleadoService(db).obtener(id_empleado)


@router.put("/{id_empleado}", response_model=EmpleadoResponse,
            summary="Actualizar empleado")
def actualizar(id_empleado: int, data: EmpleadoUpdate,
               db: Session = Depends(get_db)):
    return EmpleadoService(db).actualizar(id_empleado, data)


@router.delete("/{id_empleado}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar empleado")
def eliminar(id_empleado: int, db: Session = Depends(get_db)):
    EmpleadoService(db).eliminar(id_empleado)


# ── Estatus rápido ────────────────────────────────────────────────
@router.patch("/{id_empleado}/activar", response_model=EmpleadoResponse,
              summary="Activar empleado")
def activar(id_empleado: int, db: Session = Depends(get_db)):
    return EmpleadoService(db).activar(id_empleado)


@router.patch("/{id_empleado}/desactivar", response_model=EmpleadoResponse,
              summary="Desactivar empleado")
def desactivar(id_empleado: int, db: Session = Depends(get_db)):
    return EmpleadoService(db).desactivar(id_empleado)


# ── Roles del empleado ────────────────────────────────────────────
@router.get("/{id_empleado}/roles", response_model=list[EmpleadoRolResponse],
            summary="Ver roles asignados al empleado")
def roles(id_empleado: int, db: Session = Depends(get_db)):
    return RolService(db).listar_roles_de_empleado(id_empleado)


@router.post("/{id_empleado}/roles", response_model=EmpleadoRolResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Asignar rol al empleado")
def asignar_rol(id_empleado: int, data: AsignarRolRequest,
                db: Session = Depends(get_db)):
    return RolService(db).asignar_rol_a_empleado(id_empleado, data.id_rol)


@router.delete("/{id_empleado}/roles/{id_rol}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Quitar rol del empleado")
def quitar_rol(id_empleado: int, id_rol: int, db: Session = Depends(get_db)):
    RolService(db).quitar_rol_de_empleado(id_empleado, id_rol)