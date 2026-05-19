"""
=============================================================================
MODELO: Articulo
=============================================================================

Representa un artículo que un usuario publica para intercambiar.
Campos principales:
  - id: Identificador único
  - titulo: Nombre/título del artículo
  - descripcion: Detalles del artículo (qué es, estado, etc.)
  - categoria: Tipo de artículo (ej: "electrónica", "ropa", "libros")
  - estado: Condición del artículo (ej: "nuevo", "usado", "como nuevo")
  - disponible: Boolean que indica si está en disponible para intercambio
  - propietario_id: FK a Usuario (quién publicó el artículo)
  - creado_en: Timestamp automático

Relaciones:
  - propietario: Relación con Usuario (quién publica el artículo)
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Articulo(Base):
    """Tabla de artículos disponibles para intercambiar."""
    __tablename__ = "articulos"

    # =================================================================
    # COLUMNAS
    # =================================================================
    id = Column(Integer, primary_key=True, index=True)
    # Nombre/título del artículo
    titulo = Column(String(120), nullable=False)
    # Descripción detallada (qué es, estado, etc.)
    descripcion = Column(Text, nullable=True)
    # Categoría para búsqueda y filtrado (ej: "electrónica", "ropa")
    categoria = Column(String(60), nullable=False)
    # Estado del artículo (ej: "nuevo", "usado", "como nuevo")
    estado = Column(String(60), nullable=False)
    # Indica si el artículo sigue disponible para intercambios
    disponible = Column(Boolean, default=True, nullable=False)
    # FK a Usuario: quién es el propietario/vendedor del artículo
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    # Timestamp automático: cuándo se creó el artículo
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # =================================================================
    # RELACIONES
    # =================================================================
    # Relación con Usuario (back_populates sincroniza la relación inversa)
    propietario = relationship("Usuario", back_populates="articulos")
