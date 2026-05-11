# backend/app/core/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Construir URL de conexión MySQL
DB_USER = os.getenv("DB_USER", "erp_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "erp_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "gestion")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine síncrono (para Alembic y la mayoría de operaciones)
engine = create_engine(
    DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=20,
    pool_pre_ping=True,        # Verifica conexión antes de usar
    echo=bool(os.getenv("DB_ECHO", False))  # Log SQL solo si DB_ECHO=true
)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para modelos SQLAlchemy
Base = declarative_base()

# Dependencia para FastAPI (Obtener sesión)
def get_db() -> Session:
    """
    Generador de sesiones de BD para inyectar en endpoints.
    Asegura que la sesión se cierre al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()