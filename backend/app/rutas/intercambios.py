"""
=============================================================================
RUTAS: Intercambios
=============================================================================

Endpoints para gestión de intercambios:
- POST /intercambios - Crear solicitud de intercambio
- GET /intercambios/mios - Obtener mis intercambios (como solicitante o propietario)
- PUT /intercambios/{id}/estado - Cambiar estado de intercambio

Notas:
- Todos los endpoints requieren autenticación
- Estados válidos: "pendiente", "aceptado", "rechazado", "completado"
- Solo propietario puede aceptar/rechazar
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.intercambio import IntercambioCrear, IntercambioEstado, IntercambioSalida
from app.modelos.usuario import Usuario
from app.nucleo.dependencias import get_current_user, get_db
from app.servicios import intercambio_servicio


router = APIRouter(prefix="/intercambios", tags=["Intercambios"])


@router.post("/", response_model=IntercambioSalida, status_code=status.HTTP_201_CREATED)
def solicitar_intercambio(
    datos: IntercambioCrear,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Solicita un intercambio de un artículo.
    
    Flujo:
    1. Usuario logueado solicita intercambio de un artículo
    2. Intercambio se crea con estado "pendiente"
    3. Propietario del artículo puede aceptar/rechazar
    
    Requiere: Autenticación (JWT token)
    
    Body esperado:
    {
        "articulo_id": 1
    }
    
    Response (201): Intercambio creado
    {
        "id": 1,
        "articulo_id": 1,
        "solicitante_id": 2,
        "propietario_id": 1,
        "estado": "pendiente",
        "creado_en": "2024-01-15T10:30:00",
        "actualizado_en": null
    }
    
    Errors:
    - 400: No puedes solicitar tu propio artículo
    - 401: No autenticado
    - 404: Artículo no encontrado
    """
    return intercambio_servicio.solicitar_intercambio(
        db, articulo_id=datos.articulo_id, solicitante_id=usuario.id
    )


@router.get("/mios", response_model=List[IntercambioSalida])
def listar_mis_intercambios(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Obtiene todos los intercambios del usuario logueado.
    
    Incluye:
    - Intercambios que solicitaste (como solicitante)
    - Intercambios que otros te solicitaron (como propietario)
    
    Requiere: Autenticación (JWT token)
    
    Response (200): Lista de intercambios
    [
        {
            "id": 1,
            "articulo_id": 5,
            "solicitante_id": 2,
            "propietario_id": 1,
            "estado": "pendiente",
            "creado_en": "2024-01-15T10:30:00",
            "actualizado_en": null
        },
        ...
    ]
    
    Errors:
    - 401: No autenticado
    """
    return intercambio_servicio.listar_mis_intercambios(db, usuario_id=usuario.id)


@router.put("/{intercambio_id}/estado", response_model=IntercambioSalida)
def actualizar_estado(
    intercambio_id: int,
    datos: IntercambioEstado,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza el estado de un intercambio.
    
    Requiere: Autenticación (JWT token)
    
    Permisos:
    - "aceptado" o "rechazado": Solo el PROPIETARIO del artículo
    - "completado": Propietario O solicitante
    
    Body esperado:
    {
        "estado": "aceptado"
    }
    
    Response (200): Intercambio actualizado
    {
        "id": 1,
        "articulo_id": 1,
        "solicitante_id": 2,
        "propietario_id": 1,
        "estado": "aceptado",
        "creado_en": "2024-01-15T10:30:00",
        "actualizado_en": "2024-01-15T10:35:00"
    }
    
    Errors:
    - 401: No autenticado
    - 403: Sin permisos para cambiar a ese estado
    - 404: Intercambio no encontrado
    """
    intercambio = intercambio_servicio.obtener_intercambio(db, intercambio_id)
    if not intercambio:
        raise HTTPException(status_code=404, detail="Intercambio no encontrado")
    return intercambio_servicio.cambiar_estado(db, intercambio, datos.estado, usuario.id)
