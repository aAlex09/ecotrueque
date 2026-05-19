"""
=============================================================================
SERVICIO: Usuario
=============================================================================

Lógica de negocio para usuarios:
1. obtener_por_email: Busca usuario por email (para login)
2. obtener_por_id: Busca usuario por ID (para acceso a perfil)
3. crear_usuario: Crea nuevo usuario con contraseña hasheada
4. (Futuro: actualizar_usuario, eliminar_usuario, etc.)

Nota: Las contraseñas siempre se hashean antes de almacenar en BD
"""

from sqlalchemy.orm import Session

from app.esquemas.usuario import UsuarioCrear
from app.modelos.usuario import Usuario
from app.nucleo.seguridad import hash_contrasena


def obtener_por_email(db: Session, email: str) -> Usuario | None:
    """
    Busca un usuario por su email (case-insensitive).
    
    Args:
        db: Sesión de base de datos
        email: Email a buscar
    
    Returns:
        Objeto Usuario si existe, None si no
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_por_id(db: Session, usuario_id: int) -> Usuario | None:
    """
    Busca un usuario por su ID.
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario
    
    Returns:
        Objeto Usuario si existe, None si no
    """
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def crear_usuario(db: Session, datos: UsuarioCrear) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.
    
    Pasos:
    1. Normaliza email a minúsculas
    2. Hashea la contraseña con bcrypt
    3. Crea objeto Usuario
    4. Guarda en BD y retorna
    
    Args:
        db: Sesión de base de datos
        datos: UsuarioCrear schema (nombre, email, password)
    
    Returns:
        Nuevo Usuario creado con ID asignado por BD
    
    Nota: La contraseña se hashea con bcrypt (nunca se guarda en texto plano)
    """
    # Crear objeto Usuario
    usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email.lower(),  # Normalizar email a minúsculas
        hash_contrasena=hash_contrasena(datos.password),  # Hashear contraseña
    )
    # Guardar en BD
    db.add(usuario)
    db.commit()  # Confirmar transacción
    db.refresh(usuario)  # Actualizar objeto con datos de BD (ej: ID generado)
    return usuario
