from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class RutaEnvio(Base):

    __tablename__ = 'ruta_envio'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], ondelete='CASCADE', name='ruta_envio_ibfk_2'),
        ForeignKeyConstraint(['id_ruta'], ['ruta.id_ruta'], name='ruta_envio_ibfk_1'),
        Index('idx_re_envio', 'id_envio'),
        Index('idx_re_ruta', 'id_ruta')
    )

    id_ruta_envio: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_ruta: Mapped[int] = mapped_column(Integer, nullable=False)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)

    envios: Mapped['Envios'] = relationship('Envios', back_populates='ruta_envio')
    ruta: Mapped['Ruta'] = relationship('Ruta', back_populates='ruta_envio')

