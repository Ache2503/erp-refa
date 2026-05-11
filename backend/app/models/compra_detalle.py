from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index
import decimal
from app.core.database import Base

class CompraDetalle(Base):

    __tablename__ = 'compra_detalle'
    __table_args__ = (
        CheckConstraint('(`cantidad` > 0)', name='compra_detalle_chk_1'),
        CheckConstraint('(`precio_unitario` >= 0)', name='compra_detalle_chk_2'),
        CheckConstraint('(`subtotal` >= 0)', name='compra_detalle_chk_3'),
        ForeignKeyConstraint(['id_compra'], ['compras.id_compra'], ondelete='CASCADE', name='compra_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_movimiento'], ['movimiento.id_movimiento'], name='compra_detalle_ibfk_3'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='compra_detalle_ibfk_2'),
        Index('idx_cd_compra', 'id_compra'),
        Index('idx_cd_movimiento', 'id_movimiento'),
        Index('idx_cd_producto', 'id_producto')
    )

    id_compra_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_compra: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    id_movimiento: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    compras: Mapped['Compras'] = relationship('Compras', back_populates='compra_detalle')
    movimiento: Mapped['Movimiento'] = relationship('Movimiento', back_populates='compra_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='compra_detalle')

