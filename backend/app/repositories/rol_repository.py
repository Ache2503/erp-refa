"""
Repository — Roles & Permisos
Solo acceso a datos, sin lógica de negocio.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.roles import Roles
from app.models.permisos import Permisos
from app.models.rol_permiso import RolPermiso
from app.models.empleado_rol import EmpleadoRol
from app.schemas.roles import RolCreate, RolUpdate, PermisoCreate, PermisoUpdate


class RolRepository:

    def __init__(self, db: Session):
        self.db = db

    # ── Roles ─────────────────────────────────────────────────────

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Roles]:
        return self.db.query(Roles).offset(skip).limit(limit).all()

    def get_by_id(self, id_rol: int) -> Optional[Roles]:
        return self.db.query(Roles).filter(Roles.id_rol == id_rol).first()

    def get_by_nombre(self, nombre: str) -> Optional[Roles]:
        return self.db.query(Roles).filter(Roles.nombre == nombre).first()

    def create(self, data: RolCreate) -> Roles:
        rol = Roles(**data.model_dump())
        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def update(self, rol: Roles, data: RolUpdate) -> Roles:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rol, field, value)
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def delete(self, rol: Roles) -> None:
        self.db.delete(rol)
        self.db.commit()

    # ── Permisos ──────────────────────────────────────────────────

    def get_all_permisos(self, skip: int = 0, limit: int = 100) -> list[Permisos]:
        return self.db.query(Permisos).offset(skip).limit(limit).all()

    def get_permiso_by_id(self, id_permiso: int) -> Optional[Permisos]:
        return self.db.query(Permisos).filter(Permisos.id_permiso == id_permiso).first()

    def get_permiso_by_nombre(self, nombre: str) -> Optional[Permisos]:
        return self.db.query(Permisos).filter(Permisos.nombre == nombre).first()

    def create_permiso(self, data: PermisoCreate) -> Permisos:
        permiso = Permisos(**data.model_dump())
        self.db.add(permiso)
        self.db.commit()
        self.db.refresh(permiso)
        return permiso

    def update_permiso(self, permiso: Permisos, data: PermisoUpdate) -> Permisos:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(permiso, field, value)
        self.db.commit()
        self.db.refresh(permiso)
        return permiso

    def delete_permiso(self, permiso: Permisos) -> None:
        self.db.delete(permiso)
        self.db.commit()

    # ── Rol-Permiso ───────────────────────────────────────────────

    def get_permisos_de_rol(self, id_rol: int) -> list[Permisos]:
        return (
            self.db.query(Permisos)
            .join(RolPermiso, RolPermiso.id_permiso == Permisos.id_permiso)
            .filter(RolPermiso.id_rol == id_rol)
            .all()
        )

    def permiso_ya_asignado(self, id_rol: int, id_permiso: int) -> bool:
        return self.db.query(RolPermiso).filter(
            RolPermiso.id_rol == id_rol,
            RolPermiso.id_permiso == id_permiso,
        ).first() is not None

    def asignar_permiso(self, id_rol: int, id_permiso: int) -> RolPermiso:
        rp = RolPermiso(id_rol=id_rol, id_permiso=id_permiso)
        self.db.add(rp)
        self.db.commit()
        self.db.refresh(rp)
        return rp

    def quitar_permiso(self, id_rol: int, id_permiso: int) -> bool:
        rp = self.db.query(RolPermiso).filter(
            RolPermiso.id_rol == id_rol,
            RolPermiso.id_permiso == id_permiso,
        ).first()
        if not rp:
            return False
        self.db.delete(rp)
        self.db.commit()
        return True

    # ── Empleado-Rol ──────────────────────────────────────────────

    def get_roles_de_empleado(self, id_empleado: int) -> list[EmpleadoRol]:
        return (
            self.db.query(EmpleadoRol)
            .filter(EmpleadoRol.id_empleado == id_empleado)
            .all()
        )

    def rol_ya_asignado(self, id_empleado: int, id_rol: int) -> bool:
        return self.db.query(EmpleadoRol).filter(
            EmpleadoRol.id_empleado == id_empleado,
            EmpleadoRol.id_rol == id_rol,
        ).first() is not None

    def asignar_rol_a_empleado(self, id_empleado: int, id_rol: int) -> EmpleadoRol:
        er = EmpleadoRol(id_empleado=id_empleado, id_rol=id_rol)
        self.db.add(er)
        self.db.commit()
        self.db.refresh(er)
        return er

    def quitar_rol_de_empleado(self, id_empleado: int, id_rol: int) -> bool:
        er = self.db.query(EmpleadoRol).filter(
            EmpleadoRol.id_empleado == id_empleado,
            EmpleadoRol.id_rol == id_rol,
        ).first()
        if not er:
            return False
        self.db.delete(er)
        self.db.commit()
        return True