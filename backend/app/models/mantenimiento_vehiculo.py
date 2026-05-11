from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
import datetime
import decimal
from typing import Optional
from app.core.database import Base

class MantenimientoVehiculo(Base):

    __tablename__ = 'mantenimiento_vehiculo'
    __table_args__ = (
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='mantenimiento_vehiculo_ibfk_1'),
        Index('id_vehiculo', 'id_vehiculo')
    )

    id_mantenimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_mantenimiento: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    costo: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='mantenimiento_vehiculo')

