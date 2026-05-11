from datetime import datetime
import decimal
from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class PedidosProveedores(Base):

    __tablename__ = 'pedidos_proveedores'
    __table_args__ = (
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='pedidos_proveedores_ibfk_3'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='pedidos_proveedores_ibfk_2'),
        ForeignKeyConstraint(['id_proveedor'], ['proveedores.id_proveedor'], name='pedidos_proveedores_ibfk_1'),
        Index('id_almacen', 'id_almacen'),
        Index('idx_pp_empleado', 'id_empleado'),
        Index('idx_pp_proveedor', 'id_proveedor')
    )

    id_pedido_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_proveedor: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    impuesto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, server_default=text("'0.00'"))
    total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='pedidos_proveedores')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='pedidos_proveedores')
    proveedores: Mapped['Proveedores'] = relationship('Proveedores', back_populates='pedidos_proveedores')
    devoluciones_proveedores: Mapped[list['DevolucionesProveedores']] = relationship('DevolucionesProveedores', back_populates='pedidos_proveedores')
    pedido_proveedor_detalle: Mapped[list['PedidoProveedorDetalle']] = relationship('PedidoProveedorDetalle', back_populates='pedidos_proveedores')

