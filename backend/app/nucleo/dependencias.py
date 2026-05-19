"""
=============================================================================
DEPENDENCIAS
=============================================================================

Dependencias de FastAPI para inyección de dependencias:
1. get_db: Proporciona sesión de BD a cada endpoint
2. get_current_user: Extrae usuario del JWT token (requiere autenticación)
3. oauth2_scheme: Esquema OAuth2 para especificar dónde va el token

Concepto:
- FastAPI inyecta estas dependencias automáticamente en las rutas
- Cada request HTTP obtiene su propia sesión de BD
- Cada endpoint protegido valida el token JWT
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.nucleo.base_datos import SessionLocal
from app.nucleo.config import settings
from app.servicios import usuario_servicio


# =================================================================
# ESQUEMA OAUTH2
# =================================================================
# OAuth2PasswordBearer: Especifica que el token va en Authorization header
# tokenUrl="auth/login": La ruta donde se obtiene el token
# FastAPI automáticamente espera: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    """
    Proporciona una sesión de base de datos para cada request.
    
    Uso en rutas:
    @router.get("/")
    def mi_endpoint(db: Session = Depends(get_db)):
        # db es una sesión de BD nueva para este request
        
    Cierra automáticamente al finalizar el request (finally).
    """
    db = SessionLocal()
    try:
        # Yield: cede la sesión al endpoint
        yield db
    finally:
        # Se ejecuta después que el endpoint termina
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Valida JWT token y retorna usuario autenticado.
    
    Pasos:
    1. FastAPI extrae token del header Authorization
    2. Decodifica y valida la firma del JWT
    3. Extrae email (sub) del payload
    4. Busca usuario en BD
    5. Retorna usuario si todo es válido
    
    Uso en rutas protegidas:
    @router.post("/articulos")
    def crear(usuario: Usuario = Depends(get_current_user)):
        # usuario es el Usuario autenticado
        # Si no hay token válido → 401 Unauthorized
    
    Args:
        token: JWT token extraído del header Authorization
        db: Sesión de base de datos
    
    Returns:
        Usuario autenticado si token es válido
    
    Raises:
        HTTPException 401: Si token es inválido/expirado o usuario no existe
    """
    # Excepción genérica para credenciales inválidas
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},  # Header para cliente
    )
    
    try:
        # Decodificar JWT usando la clave secreta
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Extraer email (campo "sub") del payload
        email = payload.get("sub")
        if email is None:
            raise credenciales_invalidas
    except JWTError as exc:
        # JWT inválido, expirado o mal firmado
        raise credenciales_invalidas from exc

    # Buscar usuario en BD
    usuario = usuario_servicio.obtener_por_email(db, email=email)
    if usuario is None:
        # Token válido pero usuario fue eliminado
        raise credenciales_invalidas
    
    return usuario
