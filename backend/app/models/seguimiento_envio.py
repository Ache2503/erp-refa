import datetime
from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Column, Integer, String, Float, Date, DateTime, text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class SeguimientoEnvio(Base):

    __tablename__ = 'seguimiento_envio'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='seguimiento_envio_ibfk_1'),
        Index('idx_se_envio', 'id_envio')
    )

    id_seguimiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_seguimiento: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False)
    ubicacion: Mapped[Optional[str]] = mapped_column(String(100))

    envios: Mapped['Envios'] = relationship('Envios', back_populates='seguimiento_envio')

