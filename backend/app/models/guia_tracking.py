import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKeyConstraint, Index
from app.core.database import Base


class GuiaTracking(Base):

    __tablename__ = 'guia_tracking'
    __table_args__ = (
        ForeignKeyConstraint(['id_guia'], ['guia_remision.id_guia'], ondelete='CASCADE', name='guia_tracking_ibfk_1'),
        ForeignKeyConstraint(['id_usuario'], ['empleados.id_empleado'], name='guia_tracking_ibfk_2'),
        Index('idx_gt_guia', 'id_guia'),
        Index('idx_gt_fecha', 'fecha'),
    )

    id_tracking: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_guia: Mapped[int] = mapped_column(Integer, nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    estatus_anterior: Mapped[Optional[str]] = mapped_column(String(20))
    estatus_nuevo: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    ubicacion: Mapped[Optional[str]] = mapped_column(String(100))
    comentario: Mapped[Optional[str]] = mapped_column(Text)
