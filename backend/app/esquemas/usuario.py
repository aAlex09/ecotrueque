"""
=============================================================================
ESQUEMAS: Usuario
=============================================================================

Esquemas Pydantic para validación de datos de usuario.
- UsuarioBase: campos comunes (nombre, email)
- UsuarioCrear: para registro (hereda de Base + password)
- UsuarioActualizar: para editar perfil
- UsuarioSalida: respuesta del API (nunca incluye contraseña)

Validación: email debe ser dominio institucional
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from app.utilidades.constantes import DOMINIO_CORREO


class UsuarioBase(BaseModel):
    """Campos básicos de usuario (compartidos entre esquemas)."""
    nombre: str
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validar_dominio(cls, value: str) -> str:
        """Valida que el email sea del dominio institucional."""
        if not value.lower().endswith(DOMINIO_CORREO):
            raise ValueError(f"Solo se permite correo institucional {DOMINIO_CORREO}")
        return value


class UsuarioCrear(UsuarioBase):
    """Esquema para crear usuario (registro)."""
    password: str  # Contraseña en texto plano (FastAPI la valida, luego se hashea)


class UsuarioActualizar(BaseModel):
    """Esquema para actualizar perfil de usuario."""
    nombre: Optional[str] = None  # Campos opcionales


class UsuarioSalida(UsuarioBase):
    """Respuesta del API al consultar usuario. NUNCA incluye password."""
    id: int  # ID generado por la BD
    creado_en: Optional[datetime] = None  # Cuándo se registró

    class Config:
        # from_attributes: permite crear este schema a partir de modelos ORM
        # (transforma Usuario (ORM) → UsuarioSalida (Pydantic))
        from_attributes = True
