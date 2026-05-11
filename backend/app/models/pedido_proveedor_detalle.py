import decimal

from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class PedidoProveedorDetalle(Base):

    __tablename__ = 'pedido_proveedor_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_pedido_proveedor'], ['pedidos_proveedores.id_pedido_proveedor'], ondelete='CASCADE', name='pedido_proveedor_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='pedido_proveedor_detalle_ibfk_2'),
        Index('id_pedido_proveedor', 'id_pedido_proveedor'),
        Index('id_producto', 'id_producto')
    )

    id_pedido_proveedor_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    pedidos_proveedores: Mapped['PedidosProveedores'] = relationship('PedidosProveedores', back_populates='pedido_proveedor_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='pedido_proveedor_detalle')

