from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.rutas_service import RutaService
from app.schemas.rutas import RutaCreate, RutaResponse, RutaEnvioCreate

router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.get("", response_model=list[RutaResponse])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return RutaService(db).listar(skip, limit)

@router.post("", response_model=RutaResponse, status_code=status.HTTP_201_CREATED)
def crear(data: RutaCreate, db: Session = Depends(get_db)):
    return RutaService(db).crear(data)

@router.post("/asignar-envio")
def asignar_envio(data: RutaEnvioCreate, db: Session = Depends(get_db)):
    return RutaService(db).asignar_envio(data.id_ruta, data.id_envio)
