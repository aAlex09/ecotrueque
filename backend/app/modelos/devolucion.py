
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Devolucion(Base):
    __tablename__ = "devoluciones"

    id = Column(Integer, primary_key=True, index=True)
    intercambio_id = Column(Integer, ForeignKey("intercambios.id"), nullable=False)
    motivo = Column(Text, nullable=True)
    estado = Column(String(20), default="pendiente", nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
