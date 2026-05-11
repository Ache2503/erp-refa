from sqlalchemy import CheckConstraint, Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class ProductosAlmacen(Base):

    __tablename__ = 'productos_almacen'
    __table_args__ = (
        CheckConstraint('(`stock` >= 0)', name='productos_almacen_chk_1'),
        ForeignKeyConstraint(['id_almacen'], ['almacenes.id_almacen'], name='productos_almacen_ibfk_2'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='productos_almacen_ibfk_1'),
        Index('idx_pa_almacen', 'id_almacen'),
        Index('idx_pa_producto', 'id_producto'),
        Index('uk_producto_almacen', 'id_producto', 'id_almacen', unique=True)
    )

    id_producto_almacen: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    stock_maximo: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', back_populates='productos_almacen')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='productos_almacen')

