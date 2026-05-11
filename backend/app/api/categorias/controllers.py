"""
api/categorias/controllers.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from app.core.database import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categorias import (
    CategoriaCreate, CategoriaUpdate,
    CategoriaResponse, CategoriaListResponse,
)
router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=CategoriaListResponse)
def listar(skip: int = 0, limit: int = 100,
           db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.listar(skip=skip, limit=limit)


@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear(categoria_in: CategoriaCreate,
          db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.crear(categoria_in)


@router.get("/{id_categoria}", response_model=CategoriaResponse)
def obtener(id_categoria: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.obtener(id_categoria)


@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar(id_categoria: int, categoria_in: CategoriaUpdate,
               db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.actualizar(id_categoria, categoria_in)


@router.delete("/{id_categoria}", status_code=204)
def eliminar(id_categoria: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    service.eliminar(id_categoria)
