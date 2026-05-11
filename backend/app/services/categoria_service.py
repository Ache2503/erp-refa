"""
Service — Categorías
Maneja validaciones de unicidad de nombres.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.categoria_repository import CategoriaRepository
from app.schemas.categorias import (
    CategoriaPadreCreate, CategoriaPadreUpdate,
    CategoriaPadreResponse, CategoriaPadreConSubcategorias,
    CategoriaPadreListResponse,
    CategoriaCreate, CategoriaUpdate,
    CategoriaResponse, CategoriaConPadre, CategoriaListResponse,
)


class CategoriaService:

    def __init__(self, db: Session):
        self.repo = CategoriaRepository(db)

    # ── Categoría Padre ───────────────────────────────────────────

    def listar_padres(self, skip: int = 0,
                      limit: int = 100) -> CategoriaPadreListResponse:
        data = self.repo.get_all_padres(skip, limit)
        total = self.repo.get_total_padres()
        return CategoriaPadreListResponse(
            total=total, skip=skip, limit=limit,
            data=[CategoriaPadreResponse.model_validate(p) for p in data],
        )

    def obtener_padre(self, id_categoria_padre: int) -> CategoriaPadreResponse:
        p = self.repo.get_padre_by_id(id_categoria_padre)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría padre {id_categoria_padre} no encontrada",
            )
        return CategoriaPadreResponse.model_validate(p)

    def obtener_padre_con_subcategorias(self,
                                        id_categoria_padre: int
                                        ) -> CategoriaPadreConSubcategorias:
        p = self.repo.get_padre_by_id(id_categoria_padre)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría padre {id_categoria_padre} no encontrada",
            )
        subs = self.repo.get_by_padre(id_categoria_padre)
        data = CategoriaPadreConSubcategorias.model_validate(p)
        data.categorias = [CategoriaResponse.model_validate(s) for s in subs]
        return data

    def crear_padre(self, data: CategoriaPadreCreate) -> CategoriaPadreResponse:
        if self.repo.get_padre_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría padre con nombre '{data.nombre}'",
            )
        return CategoriaPadreResponse.model_validate(self.repo.create_padre(data))

    def actualizar_padre(self, id_categoria_padre: int,
                         data: CategoriaPadreUpdate) -> CategoriaPadreResponse:
        p = self.repo.get_padre_by_id(id_categoria_padre)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría padre {id_categoria_padre} no encontrada",
            )
        if data.nombre and data.nombre != p.nombre:
            if self.repo.get_padre_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría padre con nombre '{data.nombre}'",
                )
        return CategoriaPadreResponse.model_validate(self.repo.update_padre(p, data))

    def eliminar_padre(self, id_categoria_padre: int) -> None:
        p = self.repo.get_padre_by_id(id_categoria_padre)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría padre {id_categoria_padre} no encontrada",
            )
        self.repo.delete_padre(p)

    # ── Categoría (Subcategoría) ──────────────────────────────────

    def listar(self, skip: int = 0, limit: int = 100) -> CategoriaListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return CategoriaListResponse(
            total=total, skip=skip, limit=limit,
            data=[CategoriaResponse.model_validate(c) for c in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[CategoriaResponse]:
        return [
            CategoriaResponse.model_validate(c)
            for c in self.repo.buscar(q, skip, limit)
        ]

    def obtener(self, id_categoria: int) -> CategoriaConPadre:
        c = self.repo.get_by_id(id_categoria)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {id_categoria} no encontrada",
            )
        return CategoriaConPadre.model_validate(c)

    def listar_por_padre(self, id_categoria_padre: int,
                         skip: int = 0, limit: int = 100) -> list[CategoriaResponse]:
        if not self.repo.get_padre_by_id(id_categoria_padre):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría padre {id_categoria_padre} no encontrada",
            )
        cats = self.repo.get_by_padre(id_categoria_padre, skip, limit)
        return [CategoriaResponse.model_validate(c) for c in cats]

    def crear(self, data: CategoriaCreate) -> CategoriaResponse:
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una categoría con nombre '{data.nombre}'",
            )
        if data.id_categoria_padre:
            if not self.repo.get_padre_by_id(data.id_categoria_padre):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría padre {data.id_categoria_padre} no existe",
                )
        return CategoriaResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_categoria: int,
                   data: CategoriaUpdate) -> CategoriaResponse:
        c = self.repo.get_by_id(id_categoria)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {id_categoria} no encontrada",
            )
        if data.nombre and data.nombre != c.nombre:
            if self.repo.get_by_nombre(data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una categoría con nombre '{data.nombre}'",
                )
        if data.id_categoria_padre:
            if not self.repo.get_padre_by_id(data.id_categoria_padre):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoría padre {data.id_categoria_padre} no existe",
                )
        return CategoriaResponse.model_validate(self.repo.update(c, data))

    def eliminar(self, id_categoria: int) -> None:
        c = self.repo.get_by_id(id_categoria)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría {id_categoria} no encontrada",
            )
        self.repo.delete(c)