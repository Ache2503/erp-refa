import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Restauraciones(Base):

    __tablename__ = 'restauraciones'

    id_restauracion: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_restauracion: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

