from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(data)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
