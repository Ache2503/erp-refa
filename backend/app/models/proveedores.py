from typing import Optional

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Proveedores(Base):

    __tablename__ = 'proveedores'

    id_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))

    proveedor_contacto: Mapped[list['ProveedorContacto']] = relationship('ProveedorContacto', back_populates='proveedores')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='proveedores')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='proveedores')

