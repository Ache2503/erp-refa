import datetime
from typing import Optional
from sqlalchemy import Column, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Empleados(Base):
    __tablename__ = 'empleados'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('numero_seguridad_social', 'numero_seguridad_social', unique=True),
        Index('rfc', 'rfc', unique=True)
    )

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))
    fecha_registro: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    rfc: Mapped[Optional[str]] = mapped_column(String(13))
    numero_seguridad_social: Mapped[Optional[str]] = mapped_column(String(20))
    cargo: Mapped[Optional[str]] = mapped_column(String(50))
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))

    almacenes: Mapped[list['Almacenes']] = relationship('Almacenes', back_populates='empleados')
    auditoria: Mapped[list['Auditoria']] = relationship('Auditoria', back_populates='empleados')
    empleado_rol: Mapped[list['EmpleadoRol']] = relationship('EmpleadoRol', back_populates='empleados')
    movimiento: Mapped[list['Movimiento']] = relationship('Movimiento', back_populates='empleados')
    compras: Mapped[list['Compras']] = relationship('Compras', back_populates='empleados')
    pedidos_clientes: Mapped[list['PedidosClientes']] = relationship('PedidosClientes', back_populates='empleados')
    pedidos_proveedores: Mapped[list['PedidosProveedores']] = relationship('PedidosProveedores', back_populates='empleados')
    traslados_internos: Mapped[list['TrasladosInternos']] = relationship('TrasladosInternos', back_populates='empleados')
    envios: Mapped[list['Envios']] = relationship('Envios', back_populates='empleados')
    conductores: Mapped[list['Conductores']] = relationship('Conductores', back_populates='empleados')
