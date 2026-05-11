import decimal
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Vehiculo(Base):

    __tablename__ = 'vehiculo'
    __table_args__ = (
        ForeignKeyConstraint(['id_tipo_vehiculo'], ['tipo_vehiculo.id_tipo_vehiculo'], name='vehiculo_ibfk_1'),
        Index('idx_vehiculo_tipo', 'id_tipo_vehiculo'),
        Index('numero_serie', 'numero_serie', unique=True),
        Index('placa', 'placa', unique=True)
    )

    id_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    placa: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    id_tipo_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    modelo: Mapped[Optional[str]] = mapped_column(String(50))
    anio: Mapped[Optional[int]] = mapped_column(Integer)
    numero_serie: Mapped[Optional[str]] = mapped_column(String(50))
    capacidad_carga: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))

    tipo_vehiculo: Mapped['TipoVehiculo'] = relationship('TipoVehiculo', back_populates='vehiculo')
    mantenimiento_vehiculo: Mapped[list['MantenimientoVehiculo']] = relationship('MantenimientoVehiculo', back_populates='vehiculo')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='vehiculo')
    guia_remision: Mapped[list['GuiaRemision']] = relationship('GuiaRemision', back_populates='vehiculo')

