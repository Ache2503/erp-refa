"""
Controllers — Categorías
Jerarquía: /categoria-padres → /categorias (subcategorías)
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categorias import (
    CategoriaPadreCreate, CategoriaPadreUpdate,
    CategoriaPadreResponse, CategoriaPadreConSubcategorias,
    CategoriaPadreListResponse,
    CategoriaCreate, CategoriaUpdate,
    CategoriaResponse, CategoriaConPadre, CategoriaListResponse,
)

router = APIRouter(prefix="", tags=["Categorías"])


# ════════════════════════════════════════════════════════════════
# CATEGORÍA PADRE
# ════════════════════════════════════════════════════════════════

@router.get("/categoria-padres", response_model=CategoriaPadreListResponse,
            summary="Listar categorías padre")
def listar_padres(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CategoriaService(db).listar_padres(skip, limit)


@router.post("/categoria-padres", response_model=CategoriaPadreResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear categoría padre")
def crear_padre(data: CategoriaPadreCreate, db: Session = Depends(get_db)):
    return CategoriaService(db).crear_padre(data)


@router.get("/categoria-padres/{id_categoria_padre}",
            response_model=CategoriaPadreConSubcategorias,
            summary="Obtener categoría padre con sus subcategorías")
def obtener_padre(id_categoria_padre: int, db: Session = Depends(get_db)):
    return CategoriaService(db).obtener_padre_con_subcategorias(id_categoria_padre)


@router.put("/categoria-padres/{id_categoria_padre}",
            response_model=CategoriaPadreResponse,
            summary="Actualizar categoría padre")
def actualizar_padre(id_categoria_padre: int,
                     data: CategoriaPadreUpdate,
                     db: Session = Depends(get_db)):
    return CategoriaService(db).actualizar_padre(id_categoria_padre, data)


@router.delete("/categoria-padres/{id_categoria_padre}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar categoría padre")
def eliminar_padre(id_categoria_padre: int, db: Session = Depends(get_db)):
    CategoriaService(db).eliminar_padre(id_categoria_padre)


# ════════════════════════════════════════════════════════════════
# CATEGORÍA (SUBCATEGORÍA)
# ════════════════════════════════════════════════════════════════

@router.get("/categorias", response_model=CategoriaListResponse,
            summary="Listar categorías")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CategoriaService(db).listar(skip, limit)


@router.get("/categorias/buscar", response_model=list[CategoriaResponse],
            summary="Buscar categorías por nombre o descripción")
def buscar(
    q: str     = Query(..., min_length=1, description="Texto a buscar"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return CategoriaService(db).buscar(q, skip, limit)


@router.post("/categorias", response_model=CategoriaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear categoría")
def crear(data: CategoriaCreate, db: Session = Depends(get_db)):
    return CategoriaService(db).crear(data)


@router.get("/categorias/{id_categoria}", response_model=CategoriaConPadre,
            summary="Obtener categoría")
def obtener(id_categoria: int, db: Session = Depends(get_db)):
    return CategoriaService(db).obtener(id_categoria)


@router.put("/categorias/{id_categoria}", response_model=CategoriaResponse,
            summary="Actualizar categoría")
def actualizar(id_categoria: int, data: CategoriaUpdate,
               db: Session = Depends(get_db)):
    return CategoriaService(db).actualizar(id_categoria, data)


@router.delete("/categorias/{id_categoria}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar categoría")
def eliminar(id_categoria: int, db: Session = Depends(get_db)):
    CategoriaService(db).eliminar(id_categoria)


@router.get("/categoria-padres/{id_categoria_padre}/subcategorias",
            response_model=list[CategoriaResponse],
            summary="Listar subcategorías de una categoría padre")
def listar_subcategorias(
    id_categoria_padre: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return CategoriaService(db).listar_por_padre(id_categoria_padre, skip, limit)