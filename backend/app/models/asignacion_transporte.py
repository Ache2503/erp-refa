from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class AsignacionTransporte(Base):

    __tablename__ = 'asignacion_transporte'
    __table_args__ = (
        ForeignKeyConstraint(['id_conductor'], ['conductores.id_empleado'], name='asignacion_transporte_ibfk_2'),
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], name='asignacion_transporte_ibfk_1'),
        Index('id_envio', 'id_envio'),
        Index('idx_at_conductor', 'id_conductor')
    )

    id_asignacion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    id_conductor: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_asignacion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))

    conductores: Mapped['Conductores'] = relationship('Conductores', back_populates='asignacion_transporte')
    envios: Mapped['Envios'] = relationship('Envios', back_populates='asignacion_transporte')

