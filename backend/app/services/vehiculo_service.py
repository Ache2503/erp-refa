from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.tipo_vehiculo_repository import TipoVehiculoRepository
from app.schemas.vehiculos import (
    VehiculoCreate, VehiculoUpdate,
    VehiculoResponse, VehiculoListResponse,
)


class VehiculoService:

    def __init__(self, db: Session):
        self.repo = VehiculoRepository(db)
        self.tipo_repo = TipoVehiculoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> VehiculoListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return VehiculoListResponse(
            total=total, skip=skip, limit=limit,
            data=[VehiculoResponse.model_validate(v) for v in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[VehiculoResponse]:
        return [
            VehiculoResponse.model_validate(v)
            for v in self.repo.buscar(q, skip, limit)
        ]

    def obtener(self, id_vehiculo: int) -> VehiculoResponse:
        v = self.repo.get_by_id(id_vehiculo)
        if not v:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {id_vehiculo} no encontrado",
            )
        return VehiculoResponse.model_validate(v)

    def listar_por_tipo(self, id_tipo_vehiculo: int,
                        skip: int = 0,
                        limit: int = 100) -> list[VehiculoResponse]:
        if not self.tipo_repo.get_by_id(id_tipo_vehiculo):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {id_tipo_vehiculo} no existe",
            )
        vehiculos = self.repo.get_by_tipo(id_tipo_vehiculo, skip, limit)
        return [VehiculoResponse.model_validate(v) for v in vehiculos]

    def crear(self, data: VehiculoCreate) -> VehiculoResponse:
        if self.repo.get_by_placa(data.placa):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un vehículo con placa '{data.placa}'",
            )
        if not self.tipo_repo.get_by_id(data.id_tipo_vehiculo):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {data.id_tipo_vehiculo} no existe",
            )
        return VehiculoResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_vehiculo: int,
                   data: VehiculoUpdate) -> VehiculoResponse:
        v = self.repo.get_by_id(id_vehiculo)
        if not v:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {id_vehiculo} no encontrado",
            )
        if data.placa and data.placa != v.placa:
            if self.repo.get_by_placa(data.placa):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un vehículo con placa '{data.placa}'",
                )
        if data.id_tipo_vehiculo and data.id_tipo_vehiculo != v.id_tipo_vehiculo:
            if not self.tipo_repo.get_by_id(data.id_tipo_vehiculo):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tipo de vehículo {data.id_tipo_vehiculo} no existe",
                )
        return VehiculoResponse.model_validate(self.repo.update(v, data))

    def eliminar(self, id_vehiculo: int) -> None:
        v = self.repo.get_by_id(id_vehiculo)
        if not v:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {id_vehiculo} no encontrado",
            )
        self.repo.delete(v)
