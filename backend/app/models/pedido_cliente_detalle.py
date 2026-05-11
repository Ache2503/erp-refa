from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index
import decimal
from typing import Optional
from app.core.database import Base

class PedidoClienteDetalle(Base):

    __tablename__ = 'pedido_cliente_detalle'
    __table_args__ = (
        CheckConstraint('(`cantidad` > 0)', name='pedido_cliente_detalle_chk_1'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], ondelete='CASCADE', name='pedido_cliente_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='pedido_cliente_detalle_ibfk_2'),
        Index('idx_pcd_pedido', 'id_pedido_cliente'),
        Index('idx_pcd_producto', 'id_producto')
    )

    id_pedido_cliente_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='pedido_cliente_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='pedido_cliente_detalle')

