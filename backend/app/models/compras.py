from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index, text
import datetime
import decimal
from typing import Optional
from app.core.database import Base

class Compras(Base):

    __tablename__ = 'compras'
    __table_args__ = (
        CheckConstraint('(`subtotal` >= 0)', name='compras_chk_1'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='compras_ibfk_2'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='compras_ibfk_3'),
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='compras_ibfk_1'),
        Index('idx_compra_almacen', 'id_almacen'),
        Index('idx_compra_empleado', 'id_empleado'),
        Index('idx_compra_proveedor', 'id_proveedor')
    )

    id_compra: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_compra: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))
    tipo_comprobante: Mapped[Optional[str]] = mapped_column(String(50))
    serie: Mapped[Optional[str]] = mapped_column(String(20))
    numero: Mapped[Optional[str]] = mapped_column(String(20))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='compras')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='compras')
    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='compras')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='compras')

