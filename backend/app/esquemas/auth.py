"""
=============================================================================
ESQUEMAS: Auth
=============================================================================

Esquemas Pydantic para validación de datos de entrada/salida en autenticación.
- Validación de emails institucionales
- Validación de contraseñas
- Respuestas JWT

Pydantic garantiza que los datos cumplen el esquema antes de llegar al servicio.
"""

from pydantic import BaseModel, EmailStr, field_validator

from app.utilidades.constantes import DOMINIO_CORREO


class Registro(BaseModel):
    """Esquema para registro de nuevo usuario."""
    nombre: str
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validar_dominio(cls, value: str) -> str:
        """Valida que el email sea del dominio institucional."""
        if not value.lower().endswith(DOMINIO_CORREO):
            raise ValueError(f"Solo se permite correo institucional {DOMINIO_CORREO}")
        return value


class Login(BaseModel):
    """Esquema para login (email + contraseña)."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Respuesta del servidor con token JWT."""
    access_token: str  # JWT token para autenticación posterior
    token_type: str = "bearer"  # Tipo de token (siempre "bearer")
