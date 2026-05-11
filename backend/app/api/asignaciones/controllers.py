from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.asignaciones_service import AsignacionService
from app.schemas.asignaciones import AsignacionCreate, AsignacionResponse
from app.api.deps import get_current_user
from app.schemas.auth import UserResponse

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones"])


@router.post("", response_model=AsignacionResponse, status_code=status.HTTP_201_CREATED, summary="Asignar transportista a pedido")
def asignar(
    data: AsignacionCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return AsignacionService(db).asignar(data, current_user.id_empleado)


@router.get("/pendientes", summary="Pedidos pendientes de asignar")
def pendientes(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return AsignacionService(db).listar_pendientes(skip, limit)
