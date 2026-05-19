"""
=============================================================================
RUTAS: Usuarios
=============================================================================

Endpoints para datos de usuario:
- GET /usuarios/me - Obtener perfil del usuario logueado

Nota: El endpoint requiere autenticación (JWT token en header Authorization)
"""

from fastapi import APIRouter, Depends

from app.esquemas.usuario import UsuarioSalida
from app.nucleo.dependencias import get_current_user
from app.modelos.usuario import Usuario


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/me", response_model=UsuarioSalida)
def leer_usuario_actual(usuario: Usuario = Depends(get_current_user)):
    """
    Obtiene el perfil del usuario logueado.
    
    Requiere: JWT token válido en header
    Authorization: Bearer eyJhbGc...
    
    Response (200):
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@elpoli.edu.co",
        "creado_en": "2024-01-15T10:30:00"
    }
    
    Errors:
    - 401: No autenticado o token expirado/inválido
    """
    return usuario
