from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
import datetime
from typing import Optional
from app.core.database import Base

class CategoriaPadre(Base):

    __tablename__ = 'categoria_padre'

    id_categoria_padre: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(200))

    categorias: Mapped[list['Categorias']] = relationship('Categorias', back_populates='categoria_padre')

