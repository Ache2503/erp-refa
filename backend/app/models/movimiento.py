from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class Movimiento(Base):

    __tablename__ = 'movimiento'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['empleados.id_empleado'], name='movimiento_ibfk_1'),
        Index('idx_movimiento_fecha', 'fecha'),
        Index('idx_movimiento_usuario', 'id_usuario')
    )

    id_movimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    tipo_movimiento: Mapped[str] = mapped_column(String(20), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='movimiento')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='movimiento')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='movimiento')

