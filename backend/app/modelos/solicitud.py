
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, ForeignKey("articulos.id"), nullable=False)
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    mensaje = Column(Text, nullable=True)
    estado = Column(String(20), default="pendiente", nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
