"""
Service — Almacenes
Validaciones: unicidad de nombre, existencia de empleado y tipo_almacen
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.almacen_repository import AlmacenRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.tipo_almacen_repository import TipoAlmacenRepository
from app.schemas.almacenes import (
    AlmacenCreate, AlmacenUpdate,
    AlmacenResponse, AlmacenConRelaciones, AlmacenListResponse,
)


class AlmacenService:

    def __init__(self, db: Session):
        self.repo = AlmacenRepository(db)
        self.empleado_repo = EmpleadoRepository(db)
        self.tipo_repo = TipoAlmacenRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> AlmacenListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return AlmacenListResponse(
            total=total, skip=skip, limit=limit,
            data=[AlmacenResponse.model_validate(a) for a in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[AlmacenResponse]:
        return [
            AlmacenResponse.model_validate(a)
            for a in self.repo.buscar(q, skip, limit)
        ]

    def obtener(self, id_almacen: int) -> AlmacenConRelaciones:
        a = self.repo.get_by_id(id_almacen)
        if not a:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {id_almacen} no encontrado",
            )
        return AlmacenConRelaciones.model_validate(a)

    def listar_por_empleado(self, id_empleado: int,
                            skip: int = 0,
                            limit: int = 100) -> list[AlmacenResponse]:
        if not self.empleado_repo.get_by_id(id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no encontrado",
            )
        almacenes = self.repo.get_by_empleado(id_empleado, skip, limit)
        return [AlmacenResponse.model_validate(a) for a in almacenes]

    def listar_por_tipo(self, id_tipo_almacen: int,
                        skip: int = 0,
                        limit: int = 100) -> list[AlmacenResponse]:
        if not self.tipo_repo.get_by_id(id_tipo_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de almacén {id_tipo_almacen} no encontrado",
            )
        almacenes = self.repo.get_by_tipo(id_tipo_almacen, skip, limit)
        return [AlmacenResponse.model_validate(a) for a in almacenes]

    def crear(self, data: AlmacenCreate) -> AlmacenResponse:
        # Validar unicidad de nombre
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un almacén con nombre '{data.nombre}'",
            )
        # Validar existencia de empleado
        if not self.empleado_repo.get_by_id(data.id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {data.id_empleado} no existe",
            )
        # Validar existencia de tipo_almacen
        if not self.tipo_repo.get_by_id(data.id_tipo_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de almacén {data.id_tipo_almacen} no existe",
            )
        return AlmacenResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_almacen: int,
                   data: AlmacenUpdate) -> AlmacenResponse:
        a = self.repo.get_by_id(id_almacen)
        if not a:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {id_almacen} no encontrado",
            )
        # Validar nuevo nombre si cambió
        if data.nombre and data.nombre != a.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un almacén con nombre '{data.nombre}'",
                )
        # Validar nuevo empleado si cambió
        if data.id_empleado and data.id_empleado != a.id_empleado:
            if not self.empleado_repo.get_by_id(data.id_empleado):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Empleado {data.id_empleado} no existe",
                )
        # Validar nuevo tipo si cambió
        if data.id_tipo_almacen and data.id_tipo_almacen != a.id_tipo_almacen:
            if not self.tipo_repo.get_by_id(data.id_tipo_almacen):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tipo de almacén {data.id_tipo_almacen} no existe",
                )
        return AlmacenResponse.model_validate(self.repo.update(a, data))

    def eliminar(self, id_almacen: int) -> None:
        a = self.repo.get_by_id(id_almacen)
        if not a:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {id_almacen} no encontrado",
            )
        self.repo.delete(a)