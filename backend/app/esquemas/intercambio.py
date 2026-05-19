"""
=============================================================================
ESQUEMAS: Intercambio
=============================================================================

Esquemas Pydantic para validación de datos de intercambios.
- IntercambioCrear: para solicitar un intercambio (solo necesita articulo_id)
- IntercambioEstado: para cambiar estado de intercambio
- IntercambioSalida: respuesta del API

Validación: estado debe estar en la lista ESTADOS_INTERCAMBIO
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.utilidades.constantes import ESTADOS_INTERCAMBIO


class IntercambioCrear(BaseModel):
    """Esquema para crear una solicitud de intercambio."""
    articulo_id: int  # ID del artículo que se quiere intercambiar


class IntercambioEstado(BaseModel):
    """Esquema para actualizar el estado de un intercambio."""
    estado: str  # Nuevo estado ("pendiente", "aceptado", "rechazado", "completado")

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value: str) -> str:
        """Valida que el estado sea uno de los permitidos."""
        if value not in ESTADOS_INTERCAMBIO:
            raise ValueError(f"Estado invalido. Opciones: {ESTADOS_INTERCAMBIO}")
        return value


class IntercambioSalida(BaseModel):
    """Respuesta del API al consultar intercambios."""
    id: int  # ID de la solicitud
    articulo_id: int  # Qué artículo
    solicitante_id: int  # Quién solicita
    propietario_id: int  # Quién es dueño del artículo
    estado: str  # Estado actual ("pendiente", "aceptado", etc.)
    creado_en: Optional[datetime] = None  # Cuándo se creó la solicitud
    actualizado_en: Optional[datetime] = None  # Última actualización

    class Config:
        # Permite convertir modelo ORM a schema Pydantic
        from_attributes = True
