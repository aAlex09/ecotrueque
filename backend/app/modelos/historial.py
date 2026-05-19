
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(120), nullable=False)
    detalle = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
