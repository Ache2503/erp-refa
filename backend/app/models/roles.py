from typing import Optional

from sqlalchemy import Column, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Roles(Base):

    __tablename__ = 'roles'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    empleado_rol: Mapped[list['EmpleadoRol']] = relationship('EmpleadoRol', back_populates='roles')
    rol_permiso: Mapped[list['RolPermiso']] = relationship('RolPermiso', back_populates='roles')

