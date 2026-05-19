"""
=============================================================================
MODELO: Usuario
=============================================================================

Representa un usuario del sistema EcoTrueque.
Campos principales:
  - id: Identificador único
  - nombre: Nombre completo del usuario
  - email: Correo electrónico (único, indexado para búsquedas rápidas)
  - hash_contrasena: Contraseña hasheada con bcrypt (nunca se guarda en texto plano)
  - rol_id: FK a la tabla roles (relación con permisos)
  - creado_en: Timestamp automático de creación

Relaciones:
  - rol: Relación con modelo Rol (permisos del usuario)
  - articulos: Relación 1:N con Articulo (artículos que publica el usuario)
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.nucleo.base_datos import Base


class Usuario(Base):
    """Tabla de usuarios del sistema."""
    __tablename__ = "usuarios"

    # =================================================================
    # COLUMNAS
    # =================================================================
    id = Column(Integer, primary_key=True, index=True)
    # Nombre completo del usuario
    nombre = Column(String(120), nullable=False)
    # Email único (caso insensible) para login
    email = Column(String(150), unique=True, index=True, nullable=False)
    # Contraseña hasheada con bcrypt (nunca se guarda en texto plano)
    hash_contrasena = Column(String(255), nullable=False)
    # Referencia a tabla roles (nullable para usuarios sin rol específico)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    # Timestamp de creación automático (usa fecha/hora del servidor BD)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # =================================================================
    # RELACIONES
    # =================================================================
    # Relación con Rol (un usuario puede tener un rol)
    rol = relationship("Rol")
    # Relación con Articulo (un usuario puede tener muchos artículos)
    # back_populates sincroniza la relación inversa: articulo.propietario
    articulos = relationship("Articulo", back_populates="propietario")
