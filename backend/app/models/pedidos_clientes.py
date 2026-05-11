import datetime
import decimal
from typing import Optional

from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class PedidosClientes(Base):

    __tablename__ = 'pedidos_clientes'
    __table_args__ = (
        CheckConstraint('(`subtotal` >= 0)', name='pedidos_clientes_chk_1'),
        CheckConstraint('(`total` >= 0)', name='pedidos_clientes_chk_2'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='pedidos_clientes_ibfk_3'),
        ForeignKeyConstraint(['id_cliente'], ['clientes.id_cliente'], name='pedidos_clientes_ibfk_1'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='pedidos_clientes_ibfk_2'),
        Index('idx_pc_almacen', 'id_almacen'),
        Index('idx_pc_cliente', 'id_cliente'),
        Index('idx_pc_empleado', 'id_empleado')
    )

    id_pedido_cliente: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    impuesto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))
    requiere_envio: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='pedidos_clientes')
    clientes: Mapped['Clientes'] = relationship('Clientes', back_populates='pedidos_clientes')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='pedidos_clientes')
    devoluciones_clientes: Mapped[list['DevolucionesClientes']] = relationship('DevolucionesClientes', back_populates='pedidos_clientes')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='pedidos_clientes')
    guia_remision: Mapped[list['GuiaRemision']] = relationship('GuiaRemision', back_populates='pedidos_clientes')
    pedido_cliente_detalle: Mapped[list['PedidoClienteDetalle']] = relationship('PedidoClienteDetalle', back_populates='pedidos_clientes')