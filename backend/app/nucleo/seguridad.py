"""
=============================================================================
SEGURIDAD
=============================================================================

Funciones de seguridad:
1. hash_contrasena: Hashea contraseña con bcrypt (irreversible)
2. verificar_contrasena: Compara contraseña en texto plano con hash
3. crear_token_acceso: Genera JWT token firmado (para autenticación)

Conceptos clave:
- Bcrypt: Hash criptográfico para contraseñas (nunca se almacenan en texto plano)
- JWT: Token firmado que se envía en Authorization header
- Token contiene: email del usuario (sub) + expiración (exp)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.nucleo.config import settings


# =================================================================
# CONTEXTO DE BCRYPT
# =================================================================
# CryptContext: Gestor de hashing con bcrypt
# - schemes=["bcrypt"]: Algoritmo para hash
# - deprecated="auto": Auto-migra antiguos hashes si necesario
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_contrasena(contrasena: str) -> str:
    """
    Hashea una contraseña con bcrypt.
    
    Bcrypt es irreversible:
    - Misma contraseña → Hash diferente cada vez (por salt aleatorio)
    - No se puede recuperar la contraseña del hash
    
    Args:
        contrasena: Contraseña en texto plano
    
    Returns:
        Hash bcrypt (ej: $2b$12$...)
    """
    return pwd_context.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, hash_guardado: str) -> bool:
    """
    Verifica que una contraseña coincida con su hash.
    
    Compara:
    1. Hashea la contraseña recibida con el salt del hash guardado
    2. Compara los hashes
    
    Args:
        contrasena_plana: Contraseña en texto plano (del usuario)
        hash_guardado: Hash bcrypt almacenado en BD
    
    Returns:
        True si coinciden, False si no
    """
    return pwd_context.verify(contrasena_plana, hash_guardado)


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT token firmado.
    
    JWT (JSON Web Token):
    - Firma con SECRET_KEY
    - Contiene datos (ej: {"sub": "usuario@email.com"})
    - Incluye expiración automática
    - Frontend lo envía en Authorization header
    
    Args:
        data: Datos a incluir en el token (ej: {"sub": email})
        expires_delta: Tiempo de expiración (custom, default: settings)
    
    Returns:
        JWT token string (ej: "eyJhbGc...")
    """
    # Copiar datos a codificar
    to_encode = data.copy()
    
    # Calcular fecha de expiración
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Agregar expiración al payload
    to_encode.update({"exp": expire})
    
    # Firmar y retornar token
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
