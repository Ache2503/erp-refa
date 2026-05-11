from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError
import bcrypt

from app.core.config import settings
from app.repositories.auth_repository import AuthRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuthRepository(db)
        self.emp_repo = EmpleadoRepository(db)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def hash_password(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def create_token(self, empleado_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {"sub": str(empleado_id), "exp": expire}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    def decode_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            empleado_id = int(payload.get("sub"))
            return empleado_id
        except (JWTError, ValueError, TypeError):
            return None

    def _build_user_response(self, empleado):
        roles = self.repo.get_roles(empleado.id_empleado)
        return UserResponse(
            id_empleado=empleado.id_empleado,
            username=empleado.email,
            nombre_empleado=f"{empleado.nombre} {empleado.apellido}",
            cargo=empleado.cargo,
            roles=roles,
        )

    def login(self, data: LoginRequest) -> TokenResponse:
        empleado = self.repo.find_by_email(data.username)
        if not empleado or not empleado.password_hash:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        if not self.verify_password(data.password, empleado.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        if empleado.estatus != "activo":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta inactiva")

        token = self.create_token(empleado.id_empleado)
        user = self._build_user_response(empleado)
        return TokenResponse(access_token=token, user=user)

    def register(self, data: RegisterRequest) -> TokenResponse:
        existente = self.repo.find_by_email(data.username)
        if existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")

        password_hash = self.hash_password(data.password)
        empleado = self.repo.create_empleado(
            email=data.username,
            password_hash=password_hash,
            nombre=data.nombre,
            apellido=data.apellido,
            cargo=data.cargo,
        )
        token = self.create_token(empleado.id_empleado)
        user = self._build_user_response(empleado)
        return TokenResponse(access_token=token, user=user)

    def get_current_user(self, empleado_id: int) -> UserResponse:
        empleado = self.emp_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return self._build_user_response(empleado)
