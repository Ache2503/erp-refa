from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class TrasladoInternoDetalle(Base):

    __tablename__ = 'traslado_interno_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='traslado_interno_detalle_ibfk_2'),
        ForeignKeyConstraint(['id_traslado'], ['traslados_internos.id_traslado'], ondelete='CASCADE', name='traslado_interno_detalle_ibfk_1'),
        Index('id_producto', 'id_producto'),
        Index('id_traslado', 'id_traslado')
    )

    id_traslado_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_traslado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    productos: Mapped['Productos'] = relationship('Productos', back_populates='traslado_interno_detalle')
    traslados_internos: Mapped['TrasladosInternos'] = relationship('TrasladosInternos', back_populates='traslado_interno_detalle')

