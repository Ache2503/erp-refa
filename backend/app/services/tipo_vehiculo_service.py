"""
Service — Tipos de Vehículos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.tipo_vehiculo_repository import TipoVehiculoRepository
from app.schemas.tipos_vehiculos import (
    TipoVehiculoCreate, TipoVehiculoUpdate,
    TipoVehiculoResponse, TipoVehiculoListResponse,
)


class TipoVehiculoService:

    def __init__(self, db: Session):
        self.repo = TipoVehiculoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> TipoVehiculoListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return TipoVehiculoListResponse(
            total=total, skip=skip, limit=limit,
            data=[TipoVehiculoResponse.model_validate(tv) for tv in data],
        )

    def obtener(self, id_tipo_vehiculo: int) -> TipoVehiculoResponse:
        tv = self.repo.get_by_id(id_tipo_vehiculo)
        if not tv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {id_tipo_vehiculo} no encontrado",
            )
        return TipoVehiculoResponse.model_validate(tv)

    def crear(self, data: TipoVehiculoCreate) -> TipoVehiculoResponse:
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un tipo de vehículo con nombre '{data.nombre}'",
            )
        return TipoVehiculoResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_tipo_vehiculo: int,
                   data: TipoVehiculoUpdate) -> TipoVehiculoResponse:
        tv = self.repo.get_by_id(id_tipo_vehiculo)
        if not tv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {id_tipo_vehiculo} no encontrado",
            )
        if data.nombre and data.nombre != tv.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un tipo de vehículo con nombre '{data.nombre}'",
                )
        return TipoVehiculoResponse.model_validate(self.repo.update(tv, data))

    def eliminar(self, id_tipo_vehiculo: int) -> None:
        tv = self.repo.get_by_id(id_tipo_vehiculo)
        if not tv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {id_tipo_vehiculo} no encontrado",
            )
        self.repo.delete(tv)