from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.conductores_service import ConductorService
from app.schemas.conductores import ConductorResponse, ConductorDisponibleResponse

router = APIRouter(prefix="/conductores", tags=["Conductores"])

@router.get("", response_model=list[ConductorResponse])
def listar(db: Session = Depends(get_db)):
    return ConductorService(db).listar()

@router.get("/disponibles", response_model=list[ConductorDisponibleResponse])
def disponibles(db: Session = Depends(get_db)):
    return ConductorService(db).disponibles()
