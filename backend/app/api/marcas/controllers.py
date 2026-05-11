from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.marca_service import MarcaService
from app.schemas.marcas import MarcaCreate, MarcaUpdate, MarcaResponse

router = APIRouter(prefix="/marcas", tags=["Marcas"])


@router.get("/", response_model=list[MarcaResponse])
def listar(db: Session = Depends(get_db)):
    service = MarcaService(db)
    return service.listar()


@router.get("/{marca_id}", response_model=MarcaResponse)
def obtener(marca_id: int, db: Session = Depends(get_db)):
    service = MarcaService(db)
    marca = service.obtener(marca_id)

    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    return marca


@router.post("/", response_model=MarcaResponse, status_code=201)
def crear(data: MarcaCreate, db: Session = Depends(get_db)):
    service = MarcaService(db)
    return service.crear(data)


@router.put("/{marca_id}", response_model=MarcaResponse)
def actualizar(marca_id: int, data: MarcaUpdate, db: Session = Depends(get_db)):
    service = MarcaService(db)
    marca = service.actualizar(marca_id, data)

    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    return marca


@router.delete("/{marca_id}", status_code=204)
def eliminar(marca_id: int, db: Session = Depends(get_db)):
    service = MarcaService(db)
    eliminado = service.eliminar(marca_id)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    return None