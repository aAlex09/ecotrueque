"""
=============================================================================
BASE DE DATOS
=============================================================================

Configuración de SQLAlchemy:
- engine: Motor de base de datos (PostgreSQL)
- SessionLocal: Factory para crear sesiones
- Base: Clase base para todos los modelos ORM

Concepto:
- Un "engine" es la conexión general a la BD
- Una "Session" es una transacción individual (se abre/cierra por endpoint)
- Base es el registry de todos los modelos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.nucleo.config import settings


# =================================================================
# CONFIGURACIÓN DE ENGINE
# =================================================================
# create_engine: Crea la conexión a PostgreSQL
# pool_pre_ping=True: Verifica que la conexión sea válida antes de usarla
#   (evita problemas de conexiones muertas)
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# =================================================================
# CONFIGURACIÓN DE SESIONES
# =================================================================
# SessionLocal: Factory que crea nuevas sesiones para cada petición
# autocommit=False: Requiere commit() explícito (transacciones atómicas)
# autoflush=False: Requiere flush() explícito (mejor control)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# =================================================================
# BASE PARA MODELOS
# =================================================================
# Base: Clase padre de todos los modelos ORM
# SQLAlchemy usará esto para generar las tablas
# (ej: class Usuario(Base): ...)
Base = declarative_base()
