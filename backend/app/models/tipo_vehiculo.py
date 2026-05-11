from typing import Optional
from sqlalchemy import Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class TipoVehiculo(Base):

    __tablename__ = 'tipo_vehiculo'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_tipo_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    vehiculo: Mapped[list['Vehiculo']] = relationship('Vehiculo', back_populates='tipo_vehiculo')

