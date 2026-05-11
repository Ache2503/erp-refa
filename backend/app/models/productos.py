import decimal
from typing import Optional
from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Productos(Base):

    __tablename__ = 'productos'
    __table_args__ = (
        CheckConstraint('(`precio` >= 0)', name='productos_chk_1'),
        ForeignKeyConstraint(['id_categoria'], ['categorias.id_categoria'], name='productos_ibfk_1'),
        ForeignKeyConstraint(['id_marca'], ['marcas.id_marca'], name='productos_ibfk_2'),
        ForeignKeyConstraint(['id_unidad_medida'], ['unidades_medida.id_unidad_medida'], name='productos_ibfk_3'),
        Index('codigo', 'codigo', unique=True),
        Index('idx_producto_categoria', 'id_categoria'),
        Index('idx_producto_marca', 'id_marca'),
        Index('idx_producto_um', 'id_unidad_medida')
    )

    id_producto: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo: Mapped[str] = mapped_column(String(50), nullable=False)
    id_categoria: Mapped[int] = mapped_column(Integer, nullable=False)
    id_marca: Mapped[int] = mapped_column(Integer, nullable=False)
    id_unidad_medida: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)

    categorias: Mapped['Categorias'] = relationship('Categorias', back_populates='productos')
    marcas: Mapped['Marcas'] = relationship('Marcas', back_populates='productos')
    unidades_medida: Mapped['UnidadesMedida'] = relationship('UnidadesMedida', back_populates='productos')
    compra_detalle: Mapped[list['CompraDetalle']] = relationship('CompraDetalle', back_populates='productos')
    movimiento_detalle: Mapped[list['MovimientoDetalle']] = relationship('MovimientoDetalle', back_populates='productos')
    pedido_cliente_detalle: Mapped[list['PedidoClienteDetalle']] = relationship('PedidoClienteDetalle', back_populates='productos')
    pedido_proveedor_detalle: Mapped[list['PedidoProveedorDetalle']] = relationship('PedidoProveedorDetalle', back_populates='productos')
    productos_almacen: Mapped[list['ProductosAlmacen']] = relationship('ProductosAlmacen', back_populates='productos')
    traslado_interno_detalle: Mapped[list['TrasladoInternoDetalle']] = relationship('TrasladoInternoDetalle', back_populates='productos')
    devolucion_cliente_detalle: Mapped[list['DevolucionClienteDetalle']] = relationship('DevolucionClienteDetalle', back_populates='productos')
    devolucion_proveedor_detalle: Mapped[list['DevolucionProveedorDetalle']] = relationship('DevolucionProveedorDetalle', back_populates='productos')
    envio_detalle: Mapped[list['EnvioDetalle']] = relationship('EnvioDetalle', back_populates='productos')
    guia_remision_detalle: Mapped[list['GuiaRemisionDetalle']] = relationship('GuiaRemisionDetalle', back_populates='productos')

