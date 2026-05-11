from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import ForeignKeyConstraint, Index
from app.core.database import Base

class GuiaRemisionDetalle(Base):

    __tablename__ = 'guia_remision_detalle'
    __table_args__ = (
        ForeignKeyConstraint(['id_guia'], ['guia_remision.id_guia'], ondelete='CASCADE', name='guia_remision_detalle_ibfk_1'),
        ForeignKeyConstraint(['id_producto'], ['productos.id_producto'], name='guia_remision_detalle_ibfk_2'),
        Index('id_guia', 'id_guia'),
        Index('id_producto', 'id_producto')
    )

    id_guia_detalle: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_guia: Mapped[int] = mapped_column(Integer, nullable=False)
    id_producto: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    guia_remision: Mapped['GuiaRemision'] = relationship('GuiaRemision', back_populates='guia_remision_detalle')
    productos: Mapped['Productos'] = relationship('Productos', back_populates='guia_remision_detalle')

