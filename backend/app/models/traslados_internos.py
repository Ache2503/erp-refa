import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class TrasladosInternos(Base):

    __tablename__ = 'traslados_internos'
    __table_args__ = (
        CheckConstraint('(`id_almacen_origen` <> `id_almacen_destino`)', name='traslados_internos_chk_1'),
        ForeignKeyConstraint(['id_almacen_destino'], ['almacenes.id_almacen'], name='traslados_internos_ibfk_2'),
        ForeignKeyConstraint(['id_almacen_origen'], ['almacenes.id_almacen'], name='traslados_internos_ibfk_1'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='traslados_internos_ibfk_3'),
        Index('id_almacen_destino', 'id_almacen_destino'),
        Index('id_almacen_origen', 'id_almacen_origen'),
        Index('id_empleado', 'id_empleado')
    )

    id_traslado: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_traslado: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text('(curdate())'))
    id_almacen_origen: Mapped[int] = mapped_column(Integer, nullable=False)
    id_almacen_destino: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)

    almacenes: Mapped['Almacenes'] = relationship('Almacenes', foreign_keys=[id_almacen_destino], back_populates='traslados_internos_id_almacen_destino')
    almacenes_: Mapped['Almacenes'] = relationship('Almacenes', foreign_keys=[id_almacen_origen], back_populates='traslados_internos_id_almacen_origen')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='traslados_internos')
    traslado_interno_detalle: Mapped[list['TrasladoInternoDetalle']] = relationship('TrasladoInternoDetalle', back_populates='traslados_internos')

