"""
=============================================================================
RUTAS: Articulos
=============================================================================

Endpoints para gestión de artículos:
- GET /articulos - Listar artículos (con búsqueda opcional)
- GET /articulos/{id} - Obtener artículo específico
- POST /articulos - Crear artículo (requiere autenticación)
- PUT /articulos/{id} - Actualizar artículo (solo propietario)
- DELETE /articulos/{id} - Eliminar artículo (solo propietario)

Notas:
- Búsqueda es case-insensitive
- Solo propietario puede editar/eliminar su artículo
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.esquemas.articulo import ArticuloActualizar, ArticuloCrear, ArticuloSalida
from app.modelos.usuario import Usuario
from app.nucleo.dependencias import get_current_user, get_db
from app.servicios import articulo_servicio


router = APIRouter(prefix="/articulos", tags=["Articulos"])


@router.get("/", response_model=List[ArticuloSalida])
def listar_articulos(q: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Obtiene lista de artículos disponibles.
    
    Parámetros:
    - q (opcional): Busca en título y descripción
    
    Query example:
    GET /articulos?q=laptop
    
    Response (200):
    [
        {
            "id": 1,
            "titulo": "Laptop HP",
            "descripcion": "Laptop poco usada",
            "categoria": "Electrónica",
            "estado": "Como nuevo",
            "propietario_id": 1,
            "disponible": true,
            "creado_en": "2024-01-15T10:30:00"
        },
        ...
    ]
    """
    return articulo_servicio.listar_articulos(db, q=q)


@router.get("/{articulo_id}", response_model=ArticuloSalida)
def obtener_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un artículo específico por ID.
    
    Response (200): El artículo solicitado
    
    Errors:
    - 404: Artículo no encontrado
    """
    articulo = articulo_servicio.obtener_articulo(db, articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo no encontrado")
    return articulo


@router.post("/", response_model=ArticuloSalida, status_code=status.HTTP_201_CREATED)
def crear_articulo(
    datos: ArticuloCrear,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo artículo.
    
    Requiere: Autenticación (JWT token)
    
    Body esperado:
    {
        "titulo": "Bicicleta",
        "descripcion": "Bicicleta de montaña en perfecto estado",
        "categoria": "Deportes",
        "estado": "Como nuevo"
    }
    
    Response (201): Artículo creado con ID
    
    Errors:
    - 401: No autenticado
    """
    return articulo_servicio.crear_articulo(db, datos, propietario_id=usuario.id)


@router.put("/{articulo_id}", response_model=ArticuloSalida)
def actualizar_articulo(
    articulo_id: int,
    datos: ArticuloActualizar,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Actualiza un artículo existente.
    
    Requiere:
    - Autenticación (JWT token)
    - Ser el propietario del artículo
    
    Body esperado (todos los campos son opcionales):
    {
        "titulo": "Bicicleta de montaña",
        "estado": "Usado",
        "disponible": false
    }
    
    Response (200): Artículo actualizado
    
    Errors:
    - 401: No autenticado
    - 403: No es propietario
    - 404: Artículo no encontrado
    """
    articulo = articulo_servicio.obtener_articulo(db, articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo no encontrado")
    
    # Validar que sea el propietario
    if articulo.propietario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    return articulo_servicio.actualizar_articulo(db, articulo, datos)


@router.delete("/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_articulo(
    articulo_id: int,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Elimina un artículo.
    
    Requiere:
    - Autenticación (JWT token)
    - Ser el propietario del artículo
    
    Response (204): Sin contenido (eliminación exitosa)
    
    Errors:
    - 401: No autenticado
    - 403: No es propietario
    - 404: Artículo no encontrado
    """
    articulo = articulo_servicio.obtener_articulo(db, articulo_id)
    if not articulo:
        raise HTTPException(status_code=404, detail="Articulo no encontrado")
    
    # Validar que sea el propietario
    if articulo.propietario_id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    articulo_servicio.eliminar_articulo(db, articulo)
    return None
