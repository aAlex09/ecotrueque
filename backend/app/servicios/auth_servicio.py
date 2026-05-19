"""
=============================================================================
SERVICIO: Auth
=============================================================================

Lógica de autenticación:
1. autenticar_usuario: Verifica email y contraseña, retorna Usuario si es válido
2. crear_token_para_usuario: Genera JWT token para un usuario autenticado

Este servicio actúa como intermediario entre rutas y servicios de usuario/seguridad.
"""

from sqlalchemy.orm import Session

from app.modelos.usuario import Usuario
from app.nucleo.seguridad import crear_token_acceso, verificar_contrasena
from app.servicios import usuario_servicio


def autenticar_usuario(db: Session, email: str, password: str) -> Usuario | None:
    """
    Autentica un usuario verificando email y contraseña.
    
    Pasos:
    1. Busca usuario por email
    2. Verifica contraseña hasheada
    3. Retorna Usuario si ambas validaciones pasan, None si fallan
    
    Args:
        db: Sesión de base de datos
        email: Email del usuario (se normaliza a minúsculas)
        password: Contraseña en texto plano (será hasheada para comparar)
    
    Returns:
        Usuario si autenticación exitosa, None si falla
    """
    # Buscar usuario por email (caso insensible)
    usuario = usuario_servicio.obtener_por_email(db, email=email.lower())
    if not usuario:
        # Email no existe → autenticación fallida
        return None
    
    # Verificar que la contraseña coincida con el hash almacenado
    if not verificar_contrasena(password, usuario.hash_contrasena):
        # Contraseña incorrecta → autenticación fallida
        return None
    
    # ✓ Email y contraseña válidos
    return usuario


def crear_token_para_usuario(usuario: Usuario) -> str:
    """
    Genera un JWT token para un usuario autenticado.
    
    El token contiene:
    - "sub" (subject): email del usuario (identificador único)
    - Expiración configurada en settings (por defecto 24 horas)
    
    El frontend guarda este token y lo envía en header Authorization
    para acceder a endpoints protegidos.
    
    Args:
        usuario: Objeto Usuario autenticado
    
    Returns:
        String con el JWT token
    """
    return crear_token_acceso({"sub": usuario.email})
