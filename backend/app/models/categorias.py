from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
from typing import Optional
from datetime import datetime
from app.core.database import Base

class Categorias(Base):

    __tablename__ = 'categorias'
    __table_args__ = (
        ForeignKeyConstraint(['id_categoria_padre'], ['categoria_padre.id_categoria_padre'], name='categorias_ibfk_1'),
        Index('idx_categoria_padre', 'id_categoria_padre')
    )

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    id_categoria_padre: Mapped[Optional[int]] = mapped_column(Integer)

    categoria_padre: Mapped[Optional['CategoriaPadre']] = relationship('CategoriaPadre', back_populates='categorias')
    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='categorias')