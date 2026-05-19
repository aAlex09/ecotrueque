
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(120), nullable=False)
    cuerpo = Column(Text, nullable=False)
    leida = Column(Boolean, default=False, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
