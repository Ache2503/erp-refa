from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
from app.core.database import Base

class EnvioDetalle(Base):

    __tablename__ = 'envio_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='envio_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='envio_detalle_ibfk_2'),
        Index('id_envio', 'id_envio'),
        Index('id_producto', 'id_producto')
    )

    id_envio_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    envios: Mapped['Envios'] = relationship('Envios', back_populates='envio_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='envio_detalle')

