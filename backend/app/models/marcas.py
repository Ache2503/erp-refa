from sqlalchemy import Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime
from typing import Optional
from app.core.database import Base

class Marcas(Base):

    __tablename__ = 'marcas'
    __table_args__ = (
        Index('nombre', 'nombre', unique=True),
    )

    id_marca: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='marcas')

