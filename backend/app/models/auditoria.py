from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index, text
import datetime
from typing import Optional
from app.core.database import Base

class Auditoria(Base):

    __tablename__ = 'auditoria'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['empleados.id_empleado'], name='auditoria_ibfk_1'),
        Index('idx_auditoria_fecha', 'fecha'),
        Index('idx_auditoria_usuario', 'id_usuario')
    )

    id_auditoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    tabla: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    detalles: Mapped[Optional[str]] = mapped_column(Text)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='auditoria')

