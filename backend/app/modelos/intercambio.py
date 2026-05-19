"""
=============================================================================
MODELO: Intercambio
=============================================================================

Representa una solicitud/transacción de intercambio entre dos usuarios.
Campos:
  - id: Identificador único
  - articulo_id: FK al artículo siendo intercambiado
  - solicitante_id: FK al Usuario que solicita el intercambio
  - propietario_id: FK al Usuario que posee el artículo
  - estado: Estado del intercambio ("pendiente", "aceptado", "rechazado", "completado")
  - creado_en: Cuándo se creó la solicitud
  - actualizado_en: Cuándo fue la última actualización

Flujo típico:
  1. Usuario B ve artículo de Usuario A → crea Intercambio (estado="pendiente")
  2. Usuario A acepta/rechaza → estado cambia
  3. Si se acepta → puede cambiar a "completado"
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Intercambio(Base):
    """Tabla de intercambios/solicitudes entre usuarios."""
    __tablename__ = "intercambios"

    # =================================================================
    # COLUMNAS
    # =================================================================
    id = Column(Integer, primary_key=True, index=True)
    # FK al artículo que se quiere intercambiar
    articulo_id = Column(Integer, ForeignKey("articulos.id"), nullable=False)
    # FK al Usuario que SOLICITA el intercambio (el que quiere el artículo)
    solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    # FK al Usuario PROPIETARIO del artículo (el que publica)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    # Estado del intercambio: "pendiente", "aceptado", "rechazado", "completado"
    estado = Column(String(20), default="pendiente", nullable=False)
    # Timestamp de creación automático
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    # Timestamp de última actualización (se modifica automáticamente con onupdate)
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())

    # =================================================================
    # RELACIONES
    # =================================================================
    # Relación al artículo siendo intercambiado
    articulo = relationship("Articulo")
