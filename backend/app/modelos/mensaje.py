
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    emisor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    receptor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    contenido = Column(Text, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
