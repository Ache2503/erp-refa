from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Conductores(Base):
    __tablename__ = 'conductores'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='conductores_ibfk_1', ondelete='CASCADE'),
    )

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True)
    licencia_conducir: Mapped[str] = mapped_column(String(50), nullable=False)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='conductores')
    guia_remision: Mapped['GuiaRemision'] = relationship("GuiaRemision", back_populates="conductores")
    asignacion_transporte: Mapped[Optional['AsignacionTransporte']] = relationship('AsignacionTransporte', back_populates='conductores')
