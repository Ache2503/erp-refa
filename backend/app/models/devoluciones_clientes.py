from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class DevolucionesClientes(Base):

    __tablename__ = 'devoluciones_clientes'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='devoluciones_clientes_ibfk_1'),
        Index('id_pedido_cliente', 'id_pedido_cliente')
    )

    id_devolucion: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_devolucion: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(Text)

    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='devoluciones_clientes')
    devolucion_cliente_detalle: Mapped[list['DevolucionClienteDetalle']] = relationship('DevolucionClienteDetalle', back_populates='devoluciones_clientes')

