import datetime
from typing import Optional
from sqlalchemy import Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Clientes(Base):

    __tablename__ = 'clientes'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('rfc', 'rfc', unique=True)
    )

    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    fecha_registro: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    apellido: Mapped[Optional[str]] = mapped_column(String(100))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    rfc: Mapped[Optional[str]] = mapped_column(String(13))

    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='clientes')

