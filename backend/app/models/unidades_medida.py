from sqlalchemy import Column, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class UnidadesMedida(Base):

    __tablename__ = 'unidades_medida'
    __table_args__ = (
        Index('abreviatura', 'abreviatura', unique=True),
    )

    id_unidad_medida: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    abreviatura: Mapped[str] = mapped_column(String(10), nullable=False)

    productos: Mapped[list['Productos']] = relationship('Productos', back_populates='unidades_medida')

