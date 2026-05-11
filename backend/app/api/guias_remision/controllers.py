from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.guias_remision_service import GuiaRemisionService
from app.schemas.guias_remision import GuiaRemisionCreate, GuiaRemisionResponse, GuiaRemisionFullResponse

router = APIRouter(prefix="/guias-remision", tags=["Guías de Remisión"])


@router.get("", response_model=list[GuiaRemisionResponse])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return GuiaRemisionService(db).listar(skip, limit)


@router.get("/detalladas", response_model=list[GuiaRemisionFullResponse])
def listar_detalladas(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return GuiaRemisionService(db).listar_full(skip, limit)


@router.get("/{id_guia}", response_model=GuiaRemisionResponse)
def obtener(id_guia: int, db: Session = Depends(get_db)):
    return GuiaRemisionService(db).obtener(id_guia)


@router.get("/{id_guia}/detalle", response_model=GuiaRemisionFullResponse)
def obtener_detalle(id_guia: int, db: Session = Depends(get_db)):
    return GuiaRemisionService(db).obtener_full(id_guia)


@router.post("", response_model=GuiaRemisionResponse, status_code=status.HTTP_201_CREATED)
def crear(data: GuiaRemisionCreate, db: Session = Depends(get_db)):
    return GuiaRemisionService(db).crear(data)
