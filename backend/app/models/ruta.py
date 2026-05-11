import datetime
import decimal
from typing import Optional
from sqlalchemy import Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Ruta(Base):

    __tablename__ = 'ruta'

    id_ruta: Mapped[int] = mapped_column(Integer, primary_key=True)
    origen: Mapped[str] = mapped_column(String(100), nullable=False)
    destino: Mapped[str] = mapped_column(String(100), nullable=False)
    distancia: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 2))
    tiempo_estimado: Mapped[Optional[datetime.time]] = mapped_column(Time)

    ruta_envio: Mapped[list['RutaEnvio']] = relationship('RutaEnvio', back_populates='ruta')

