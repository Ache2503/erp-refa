from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
from app.core.database import Base

class EmpleadoRol(Base):

    __tablename__ = 'empleado_rol'
    __table_args__ = (
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], ondelete='CASCADE', name='empleado_rol_ibfk_1'),
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ondelete='CASCADE', name='empleado_rol_ibfk_2'),
        Index('id_rol', 'id_rol'),
        Index('uk_empleado_rol', 'id_empleado', 'id_rol', unique=True)
    )

    id_empleado_rol: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)

    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='empleado_rol')
    roles: Mapped['Roles'] = relationship('Roles', back_populates='empleado_rol')

