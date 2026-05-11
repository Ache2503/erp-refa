from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
import datetime
from typing import Optional
from app.core.database import Base

class Backups(Base):

    __tablename__ = 'backups'

    id_backup: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_backup: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    ruta_archivo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

