from typing import Optional
from sqlalchemy import Column, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class TiposAlmacen(Base):

    __tablename__ = 'tipos_almacen'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_tipo_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    almacenes: Mapped[list['Almacenes']] = relationship('Almacenes', back_populates='tipos_almacen')

