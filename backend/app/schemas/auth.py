from pydantic import BaseModel, Field
from typing import Optional, List

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)
    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    cargo: Optional[str] = None

class UserResponse(BaseModel):
    id_empleado: int
    username: str
    nombre_empleado: str
    cargo: Optional[str] = None
    roles: List[str] = []

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
