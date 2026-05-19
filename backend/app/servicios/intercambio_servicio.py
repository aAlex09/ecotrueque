"""
=============================================================================
SERVICIO: Intercambio
=============================================================================

Lógica de negocio para intercambios:
1. solicitar_intercambio: Crea solicitud de intercambio (validaciones)
2. listar_mis_intercambios: Obtiene intercambios donde usuario es solicitante o propietario
3. obtener_intercambio: Obtiene un intercambio específico
4. cambiar_estado: Actualiza estado (con validaciones de permisos)

Estados válidos:
- "pendiente": Solicitud nueva, esperando respuesta del propietario
- "aceptado": Propietario aceptó el intercambio
- "rechazado": Propietario rechazó el intercambio
- "completado": Intercambio finalizado
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modelos.articulo import Articulo
from app.modelos.intercambio import Intercambio


def solicitar_intercambio(
    db: Session, articulo_id: int, solicitante_id: int
) -> Intercambio:
    """
    Crea una solicitud de intercambio.
    
    Validaciones:
    - Artículo debe existir
    - Usuario no puede solicitar su propio artículo
    
    Args:
        db: Sesión de base de datos
        articulo_id: ID del artículo a intercambiar
        solicitante_id: ID del usuario que solicita
    
    Returns:
        Nuevo Intercambio con estado "pendiente"
    
    Raises:
        HTTPException 404: Si artículo no existe
        HTTPException 400: Si intenta su propio artículo
    """
    # Verificar que el artículo existe
    articulo = db.query(Articulo).filter(Articulo.id == articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo no encontrado")
    
    # Validar que no sea tu propio artículo
    if articulo.propietario_id == solicitante_id:
        raise HTTPException(
            status_code=400, detail="No puedes solicitar tu propio articulo"
        )
    
    # Crear intercambio en estado "pendiente"
    intercambio = Intercambio(
        articulo_id=articulo_id,
        solicitante_id=solicitante_id,
        propietario_id=articulo.propietario_id,
        estado="pendiente",
    )
    db.add(intercambio)
    db.commit()
    db.refresh(intercambio)
    return intercambio


def listar_mis_intercambios(db: Session, usuario_id: int) -> list[Intercambio]:
    """
    Obtiene todos los intercambios del usuario.
    
    Retorna intercambios donde el usuario es:
    - Solicitante: pidió un artículo
    - Propietario: alguien le pidió uno de sus artículos
    
    Ordena por fecha (más recientes primero).
    
    Args:
        db: Sesión de base de datos
        usuario_id: ID del usuario logueado
    
    Returns:
        Lista de intercambios ordenada por fecha desc
    """
    return (
        db.query(Intercambio)
        .filter(
            # Intercambios donde es solicitante O propietario
            (Intercambio.solicitante_id == usuario_id)
            | (Intercambio.propietario_id == usuario_id)
        )
        .order_by(Intercambio.creado_en.desc())
        .all()
    )


def obtener_intercambio(db: Session, intercambio_id: int) -> Intercambio | None:
    """
    Obtiene un intercambio específico por ID.
    
    Args:
        db: Sesión de base de datos
        intercambio_id: ID del intercambio
    
    Returns:
        Intercambio si existe, None si no
    """
    return db.query(Intercambio).filter(Intercambio.id == intercambio_id).first()


def cambiar_estado(
    db: Session, intercambio: Intercambio, nuevo_estado: str, actor_id: int
) -> Intercambio:
    """
    Cambia el estado de un intercambio (con validaciones de permisos).
    
    Reglas de permisos:
    - "aceptado" o "rechazado": Solo el PROPIETARIO (dueño del artículo)
    - "completado": Propietario O solicitante (ambos pueden marcar como hecho)
    
    Args:
        db: Sesión de base de datos
        intercambio: Objeto Intercambio a actualizar
        nuevo_estado: Nuevo estado ("pendiente", "aceptado", "rechazado", "completado")
        actor_id: ID del usuario que hace la acción (para validar permisos)
    
    Returns:
        Intercambio actualizado
    
    Raises:
        HTTPException 403: Si no tiene permisos para cambiar a ese estado
    """
    # Solo propietario puede aceptar/rechazar
    if nuevo_estado in ["aceptado", "rechazado"] and actor_id != intercambio.propietario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el propietario puede aceptar o rechazar",
        )
    
    # Solo propietario o solicitante pueden marcar como completado
    if nuevo_estado == "completado" and actor_id not in (
        intercambio.propietario_id,
        intercambio.solicitante_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado para completar",
        )

    # Actualizar estado
    intercambio.estado = nuevo_estado
    db.commit()
    db.refresh(intercambio)
    return intercambio
