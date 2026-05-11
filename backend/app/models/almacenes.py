from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, Index
from typing import Optional
from app.core.database import Base

class Almacenes(Base):

    __tablename__ = 'almacenes'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='almacenes_ibfk_1'),
        ForeignKeyConstraint(['id_tipo_almacen'], ['tipos_almacen.id_tipo_almacen'], name='almacenes_ibfk_2'),
        Index('idx_almacen_empleado', 'id_empleado'),
        Index('idx_almacen_tipo', 'id_tipo_almacen')
    )

    id_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_tipo_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(200))

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='almacenes')
    tipos_almacen: Mapped['TiposAlmacen'] = relationship('TiposAlmacen', back_populates='almacenes')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='almacenes')
    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='almacenes')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='almacenes')
    traslados_internos_id_almacen_destino: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', foreign_keys='[TrasladosInternos.id_almacen_destino]', back_populates='almacenes')
    traslados_internos_id_almacen_origen: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', foreign_keys='[TrasladosInternos.id_almacen_origen]', back_populates='almacenes_')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='almacenes')
    productos_almacen: Mapped[list['ProductosAlmacen']] = relationship('ProductosAlmacen', back_populates='almacenes')

