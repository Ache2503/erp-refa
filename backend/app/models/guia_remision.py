from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class GuiaRemision(Base):

    __tablename__ = 'guia_remision'
    __table_args__ = (
        ForeignKeyConstraint(['id_conductor'], ['conductores.id_empleado'], name='guia_remision_ibfk_3'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='guia_remision_ibfk_1'),
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='guia_remision_ibfk_2'),
        Index('id_pedido_cliente', 'id_pedido_cliente'),
        Index('idx_gr_conductor', 'id_conductor'),
        Index('idx_gr_vehiculo', 'id_vehiculo')
    )

    id_guia: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_guia: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    id_conductor: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)

    conductores: Mapped['Conductores'] = relationship('Conductores', back_populates='guia_remision')
    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='guia_remision')
    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='guia_remision')
    guia_remision_detalle: Mapped[list['GuiaRemisionDetalle']] = relationship('GuiaRemisionDetalle', back_populates='guia_remision')

