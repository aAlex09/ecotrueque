"""
=============================================================================
MODELO: Rol
=============================================================================

Representa los roles/permisos en el sistema.
Campos:
  - id: Identificador único
  - nombre: Nombre del rol (ej: "usuario", "admin")
  - descripcion: Descripción de qué permisos tiene el rol

Este modelo es simple y permite una futura extensión para permisos granulares.
"""

from sqlalchemy import Column, Integer, String

from app.nucleo.base_datos import Base


class Rol(Base):
    """Tabla de roles del sistema."""
    __tablename__ = "roles"

    # =================================================================
    # COLUMNAS
    # =================================================================
    id = Column(Integer, primary_key=True, index=True)
    # Nombre único del rol (ej: "usuario", "admin", "moderador")
    nombre = Column(String(50), unique=True, nullable=False)
    # Descripción del rol y sus permisos
    descripcion = Column(String(200), nullable=True)
