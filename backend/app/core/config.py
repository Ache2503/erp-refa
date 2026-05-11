"""
Configuración central de la aplicación FastAPI
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings"""

    # Información de la App
    app_name: str = "ERP API"
    app_version: str = "0.1.0"

    # ─── Base de Datos (variables individuales desde .env / Docker) ───
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "erp_user"
    db_password: str = "erp_pass"
    db_name: str = "gestion"

    # database_url se construye automáticamente si no se provee
    database_url: Optional[str] = None

    # ─── Redis ────────────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ─── Seguridad JWT ────────────────────────────────────────────────
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # ─── CORS ─────────────────────────────────────────────────────────
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # ─── Entorno ──────────────────────────────────────────────────────
    environment: str = "development"
    debug: bool = True

    def get_database_url(self) -> str:
        """Retorna la URL de conexión a MySQL para SQLAlchemy"""
        if self.database_url:
            return self.database_url
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignora variables del .env no declaradas


settings = Settings()