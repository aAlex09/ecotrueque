"""
=============================================================================
SERVICIO: Articulo
=============================================================================

Lógica de negocio para artículos:
1. crear_articulo: Crea nuevo artículo (solo el propietario)
2. listar_articulos: Obtiene todos los artículos con búsqueda opcional
3. obtener_articulo: Obtiene un artículo específico por ID
4. actualizar_articulo: Actualiza campos de un artículo (partial update)
5. eliminar_articulo: Elimina un artículo de la BD

Nota: No hay restricciones de permisos aquí (se validan en las rutas)
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.esquemas.articulo import ArticuloActualizar, ArticuloCrear
from app.modelos.articulo import Articulo


def crear_articulo(db: Session, datos: ArticuloCrear, propietario_id: int) -> Articulo:
    """
    Crea un nuevo artículo.
    
    Args:
        db: Sesión de base de datos
        datos: ArticuloCrear schema (titulo, descripcion, categoria, estado)
        propietario_id: ID del usuario que publica el artículo
    
    Returns:
        Nuevo Articulo creado con ID asignado por BD
    """
    # Crear objeto Articulo con datos validados
    articulo = Articulo(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        categoria=datos.categoria,
        estado=datos.estado,
        propietario_id=propietario_id,
    )
    # Guardar en BD
    db.add(articulo)
    db.commit()
    db.refresh(articulo)
    return articulo


def listar_articulos(db: Session, q: str | None = None) -> list[Articulo]:
    """
    Obtiene lista de artículos con búsqueda opcional.
    
    Búsqueda:
    - Si 'q' está vacío: retorna todos los artículos
    - Si 'q' tiene valor: busca en titulo o descripcion (case-insensitive)
    
    Ordena por fecha de creación (más recientes primero).
    
    Args:
        db: Sesión de base de datos
        q: Query string de búsqueda (opcional)
    
    Returns:
        Lista de artículos ordenados por fecha desc
    """
    # Consulta base
    consulta = db.query(Articulo)
    
    # Filtrar por búsqueda si existe
    if q:
        like = f"%{q}%"  # Patrón SQL LIKE (cualquier cosa + q + cualquier cosa)
        # Busca en titulo O descripcion (case-insensitive con ilike)
        consulta = consulta.filter(
            or_(Articulo.titulo.ilike(like), Articulo.descripcion.ilike(like))
        )
    
    # Ordenar por más recientes primero
    return consulta.order_by(Articulo.creado_en.desc()).all()


def obtener_articulo(db: Session, articulo_id: int) -> Articulo | None:
    """
    Obtiene un artículo específico por ID.
    
    Args:
        db: Sesión de base de datos
        articulo_id: ID del artículo
    
    Returns:
        Articulo si existe, None si no
    """
    return db.query(Articulo).filter(Articulo.id == articulo_id).first()


def actualizar_articulo(
    db: Session, articulo: Articulo, datos: ArticuloActualizar
) -> Articulo:
    """
    Actualiza un artículo existente.
    
    Nota: Solo actualiza campos que vienen en 'datos' (partial update).
    Usa model_dump(exclude_unset=True) para no sobrescribir campos no enviados.
    
    Args:
        db: Sesión de base de datos
        articulo: Objeto Articulo a actualizar
        datos: ArticuloActualizar schema (campos opcionales)
    
    Returns:
        Articulo actualizado
    """
    # Convertir schema Pydantic a diccionario (solo campos que vienen)
    datos_dict = datos.model_dump(exclude_unset=True)
    
    # Actualizar cada campo
    for campo, valor in datos_dict.items():
        setattr(articulo, campo, valor)
    
    # Guardar cambios
    db.commit()
    db.refresh(articulo)
    return articulo


def eliminar_articulo(db: Session, articulo: Articulo) -> None:
    """
    Elimina un artículo de la base de datos.
    
    Args:
        db: Sesión de base de datos
        articulo: Objeto Articulo a eliminar
    """
    db.delete(articulo)
    db.commit()
