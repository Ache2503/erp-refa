import decimal
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
import datetime
from app.core.database import Base

class MovimientoDetalle(Base):

    __tablename__ = 'movimiento_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='movimiento_detalle_ibfk_3'),
        ForeignKeyConstraint(['id_movimiento'], ['movimiento.id_movimiento'], ondelete='CASCADE', name='movimiento_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='movimiento_detalle_ibfk_2'),
        Index('idx_md_almacen', 'id_almacen'),
        Index('idx_md_movimiento', 'id_movimiento'),
        Index('idx_md_producto', 'id_producto')
    )

    id_movimiento_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_movimiento: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='movimiento_detalle')
    movimiento: Mapped['Movimiento'] = relationship('Movimiento', back_populates='movimiento_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='movimiento_detalle')

