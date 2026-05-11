from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class RolPermiso(Base):

    __tablename__ = 'rol_permiso'
    __table_args__ = (
        ForeignKeyConstraint(['id_permiso'], ['permisos.id_permiso'], ondelete='CASCADE', name='rol_permiso_ibfk_2'),
        ForeignKeyConstraint(['id_rol'], ['roles.id_rol'], ondelete='CASCADE', name='rol_permiso_ibfk_1'),
        Index('id_permiso', 'id_permiso'),
        Index('uk_rol_permiso', 'id_rol', 'id_permiso', unique=True)
    )

    id_rol_permiso: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_rol: Mapped[int] = mapped_column(Integer, nullable=False)
    id_permiso: Mapped[int] = mapped_column(Integer, nullable=False)

    permisos: Mapped['Permisos'] = relationship('Permisos', back_populates='rol_permiso')
    roles: Mapped['Roles'] = relationship('Roles', back_populates='rol_permiso')

