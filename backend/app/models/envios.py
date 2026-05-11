from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class Envios(Base):

    __tablename__ = 'envios'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='envios_ibfk_3'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='envios_ibfk_1'),
        ForeignKeyConstraint(['id_vehiculo'], ['vehiculo.id_vehiculo'], name='envios_ibfk_2'),
        Index('id_empleado', 'id_empleado'),
        Index('idx_envio_vehiculo', 'id_vehiculo'),
        Index('uk_envio_pedido', 'id_pedido_cliente', unique=True)
    )

    id_envio: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_envio: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_vehiculo: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='envios')
    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='envios')
    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', back_populates='envios')
    asignacion_transporte: Mapped[list['AsignacionTransporte']] = relationship('AsignacionTransporte', back_populates='envios')
    envio_detalle: Mapped[list['EnvioDetalle']] = relationship('EnvioDetalle', back_populates='envios')
    ruta_envio: Mapped[list['RutaEnvio']] = relationship('RutaEnvio', back_populates='envios')
    seguimiento_envio: Mapped[list['SeguimientoEnvio']] = relationship('SeguimientoEnvio', back_populates='envios')

