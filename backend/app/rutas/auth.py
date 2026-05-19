"""
=============================================================================
RUTAS: Auth
=============================================================================

Endpoints para autenticación:
- POST /auth/registro - Registrar nuevo usuario
- POST /auth/login - Login y obtener JWT token

Notas:
- El login usa OAuth2PasswordRequestForm (username/password es estándar FastAPI)
- Retorna JWT token que el frontend guarda y envía en headers
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.esquemas.auth import Token
from app.esquemas.usuario import UsuarioCrear, UsuarioSalida
from app.nucleo.dependencias import get_db
from app.servicios import auth_servicio, usuario_servicio


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registro", response_model=UsuarioSalida, status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: UsuarioCrear, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    
    Flujo:
    1. Recibe nombre, email, password (schema UsuarioCrear lo valida)
    2. Verifica que email no esté registrado
    3. Crea usuario (contraseña se hashea automáticamente)
    4. Retorna datos del usuario (nunca la contraseña)
    
    Body esperado:
    {
        "nombre": "Juan Pérez",
        "email": "juan@elpoli.edu.co",
        "password": "MiContraseña123"
    }
    
    Response (201):
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "email": "juan@elpoli.edu.co",
        "creado_en": "2024-01-15T10:30:00"
    }
    """
    # Validar que email no esté registrado
    if usuario_servicio.obtener_por_email(db, email=datos.email.lower()):
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")
    
    # Crear usuario (servicio hashea contraseña automáticamente)
    return usuario_servicio.crear_usuario(db, datos)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login: autentica usuario y retorna JWT token.
    
    Flujo:
    1. Recibe email (como username) y password (formulario estándar)
    2. Autentica usuario (valida email + contraseña)
    3. Si es válido: crea JWT token y lo retorna
    4. Frontend guarda token y lo envía en Authorization header
    
    Form esperado (application/x-www-form-urlencoded):
    - username: juan@elpoli.edu.co
    - password: MiContraseña123
    
    Response (200):
    {
        "access_token": "eyJhbGc...",
        "token_type": "bearer"
    }
    
    Errors:
    - 400: Email o contraseña incorrectos
    """
    # Autenticar usuario (verifica email + password)
    usuario = auth_servicio.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas",
        )
    
    # Generar JWT token
    token = auth_servicio.crear_token_para_usuario(usuario)
    return {"access_token": token, "token_type": "bearer"}
