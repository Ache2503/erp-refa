"""
Service — Unidades de Medida
Validaciones de unicidad: nombre y abreviatura.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.unidad_medida_repository import UnidadMedidaRepository
from app.schemas.unidades_medida import (
    UnidadMedidaCreate, UnidadMedidaUpdate,
    UnidadMedidaResponse, UnidadMedidaListResponse,
)


class UnidadMedidaService:

    def __init__(self, db: Session):
        self.repo = UnidadMedidaRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> UnidadMedidaListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return UnidadMedidaListResponse(
            total=total, skip=skip, limit=limit,
            data=[UnidadMedidaResponse.model_validate(um) for um in data],
        )

    def obtener(self, id_unidad_medida: int) -> UnidadMedidaResponse:
        um = self.repo.get_by_id(id_unidad_medida)
        if not um:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unidad de medida {id_unidad_medida} no encontrada",
            )
        return UnidadMedidaResponse.model_validate(um)

    def crear(self, data: UnidadMedidaCreate) -> UnidadMedidaResponse:
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una unidad con nombre '{data.nombre}'",
            )
        if self.repo.get_by_abreviatura(data.abreviatura):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una unidad con abreviatura '{data.abreviatura}'",
            )
        return UnidadMedidaResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_unidad_medida: int,
                   data: UnidadMedidaUpdate) -> UnidadMedidaResponse:
        um = self.repo.get_by_id(id_unidad_medida)
        if not um:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unidad de medida {id_unidad_medida} no encontrada",
            )
        if data.nombre and data.nombre != um.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una unidad con nombre '{data.nombre}'",
                )
        if data.abreviatura and data.abreviatura != um.abreviatura:
            if self.repo.get_by_abreviatura(data.abreviatura):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una unidad con abreviatura '{data.abreviatura}'",
                )
        return UnidadMedidaResponse.model_validate(self.repo.update(um, data))

    def eliminar(self, id_unidad_medida: int) -> None:
        um = self.repo.get_by_id(id_unidad_medida)
        if not um:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unidad de medida {id_unidad_medida} no encontrada",
            )
        self.repo.delete(um)