"""
Service — Vehículos
Validaciones: unicidad de placa, existencia de tipo y conductor
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.tipo_vehiculo_repository import TipoVehiculoRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.vehiculos import (
    VehiculoCreate, VehiculoUpdate,
    VehiculoResponse, VehiculoConRelaciones, VehiculoListResponse,
)


class VehiculoService:

    def __init__(self, db: Session):
        self.repo = VehiculoRepository(db)
        self.tipo_repo = TipoVehiculoRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

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

    def obtener(self, id_vehiculo: int) -> VehiculoConRelaciones:
        v = self.repo.get_by_id(id_vehiculo)
        if not v:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehículo {id_vehiculo} no encontrado",
            )
        return VehiculoConRelaciones.model_validate(v)

    def listar_por_conductor(self, id_conductor: int,
                             skip: int = 0,
                             limit: int = 100) -> list[VehiculoResponse]:
        if not self.empleado_repo.get_by_id(id_conductor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conductor {id_conductor} no existe",
            )
        vehiculos = self.repo.get_by_conductor(id_conductor, skip, limit)
        return [VehiculoResponse.model_validate(v) for v in vehiculos]

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

    def listar_por_estado(self, estado: str,
                          skip: int = 0,
                          limit: int = 100) -> list[VehiculoResponse]:
        estados_validos = ["activo", "inactivo", "mantenimiento"]
        if estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
            )
        vehiculos = self.repo.get_by_estado(estado, skip, limit)
        return [VehiculoResponse.model_validate(v) for v in vehiculos]

    def crear(self, data: VehiculoCreate) -> VehiculoResponse:
        # Validar unicidad de placa
        if self.repo.get_by_placa(data.placa):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un vehículo con placa '{data.placa}'",
            )
        # Validar existencia de tipo
        if not self.tipo_repo.get_by_id(data.id_tipo_vehiculo):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de vehículo {data.id_tipo_vehiculo} no existe",
            )
        # Validar existencia de conductor
        if not self.empleado_repo.get_by_id(data.id_conductor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conductor {data.id_conductor} no existe",
            )
        # Validar estado
        estados_validos = ["activo", "inactivo", "mantenimiento"]
        if data.estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
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
        # Validar nueva placa si cambió
        if data.placa and data.placa != v.placa:
            if self.repo.get_by_placa(data.placa):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un vehículo con placa '{data.placa}'",
                )
        # Validar nuevo tipo si cambió
        if data.id_tipo_vehiculo and data.id_tipo_vehiculo != v.id_tipo_vehiculo:
            if not self.tipo_repo.get_by_id(data.id_tipo_vehiculo):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tipo de vehículo {data.id_tipo_vehiculo} no existe",
                )
        # Validar nuevo conductor si cambió
        if data.id_conductor and data.id_conductor != v.id_conductor:
            if not self.empleado_repo.get_by_id(data.id_conductor):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conductor {data.id_conductor} no existe",
                )
        # Validar estado si cambió
        if data.estado:
            estados_validos = ["activo", "inactivo", "mantenimiento"]
            if data.estado not in estados_validos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
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