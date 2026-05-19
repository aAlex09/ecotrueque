
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    emisor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    receptor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    puntaje = Column(Integer, nullable=False)
    comentario = Column(String(255), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
