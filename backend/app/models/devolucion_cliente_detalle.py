from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
from app.core.database import Base

class DevolucionClienteDetalle(Base):

    __tablename__ = 'devolucion_cliente_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_devolucion'], ['devoluciones_clientes.id_devolucion'], ondelete='CASCADE', name='devolucion_cliente_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='devolucion_cliente_detalle_ibfk_2'),
        Index('id_devolucion', 'id_devolucion'),
        Index('id_producto', 'id_producto')
    )

    id_devolucion_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_devolucion: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    devoluciones_clientes: Mapped['DevolucionesClientes'] = relationship('DevolucionesClientes', back_populates='devolucion_cliente_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='devolucion_cliente_detalle')

