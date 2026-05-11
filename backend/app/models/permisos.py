from typing import Optional
from sqlalchemy import Column, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Permisos(Base):

    __tablename__ = 'permisos'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    rol_permiso: Mapped[list['RolPermiso']] = relationship('RolPermiso', back_populates='permisos')