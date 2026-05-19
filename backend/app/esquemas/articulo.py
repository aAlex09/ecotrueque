"""
=============================================================================
ESQUEMAS: Articulo
=============================================================================

Esquemas Pydantic para validación de datos de artículos.
- ArticuloBase: campos comunes
- ArticuloCrear: para crear un artículo (sin ID, propietario_id ni timestamps)
- ArticuloActualizar: para editar artículo (todos los campos opcionales)
- ArticuloSalida: respuesta del API (incluye ID, propietario_id, timestamps)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticuloBase(BaseModel):
    """Campos básicos de un artículo."""
    titulo: str
    descripcion: Optional[str] = None  # Descripción detallada
    categoria: str  # Tipo de artículo (ej: "electrónica", "ropa")
    estado: str  # Condición (ej: "nuevo", "usado", "como nuevo")


class ArticuloCrear(ArticuloBase):
    """Esquema para crear artículo. El servidor genera ID, propietario_id y timestamps."""
    pass


class ArticuloActualizar(BaseModel):
    """Esquema para actualizar artículo. Todos los campos son opcionales."""
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    estado: Optional[str] = None
    disponible: Optional[bool] = None  # Se puede marcar como no disponible


class ArticuloSalida(ArticuloBase):
    """Respuesta del API al consultar artículos."""
    id: int  # ID generado por BD
    propietario_id: int  # Quién publica el artículo
    disponible: bool  # Si está disponible para intercambiar
    creado_en: Optional[datetime] = None  # Cuándo se publicó

    class Config:
        # Permite convertir modelo ORM (Articulo) a schema Pydantic
        from_attributes = True
