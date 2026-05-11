from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Index
from typing import Optional
import datetime
from app.core.database import Base

class Configuracion(Base):

    __tablename__ = 'configuracion'
    __table_args__ = (
        Index('clave', 'clave', unique=True),
    )

    id_configuracion: Mapped[int] = mapped_column(Integer, primary_key=True)
    clave: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

