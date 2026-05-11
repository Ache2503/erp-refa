from typing import Optional

from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class ProveedorContacto(Base):

    __tablename__ = 'proveedor_contacto'
    __table_args__ = (
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='proveedor_contacto_ibfk_1'),
        Index('idx_contacto_proveedor', 'id_proveedor')
    )

    id_contacto: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(100))

    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='proveedor_contacto')

