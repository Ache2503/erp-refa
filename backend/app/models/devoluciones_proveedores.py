from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class DevolucionesProveedores(Base):

    __tablename__ = 'devoluciones_proveedores'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_proveedor'], ['pedidos_proveedores.id_pedido_proveedor'], name='devoluciones_proveedores_ibfk_1'),
        Index('id_pedido_proveedor', 'id_pedido_proveedor')
    )

    id_devolucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_devolucion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(Text)

    pedidos_proveedores: Mapped['PedidosProveedores'] = relationship('PedidosProveedores', back_populates='devoluciones_proveedores')
    devolucion_proveedor_detalle: Mapped[list['DevolucionProveedorDetalle']] = relationship('DevolucionProveedorDetalle', back_populates='devoluciones_proveedores')

