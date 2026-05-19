"""
=============================================================================
MAIN - Punto de entrada de la aplicación FastAPI
=============================================================================

Este módulo configura e inicializa la aplicación FastAPI:
- Configuración de CORS para permitir acceso desde el frontend
- Creación automática de tablas en la base de datos
- Carga de datos iniciales (seed)
- Registro de rutas (auth, usuarios, artículos, intercambios)

La aplicación sigue una arquitectura en capas:
  Rutas (endpoints) → Servicios (lógica) → Modelos (BD) → Base de datos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.nucleo.base_datos import Base, SessionLocal, engine
from app.nucleo.config import settings
# Importar rutas activas
from app.rutas import articulos, auth, intercambios, usuarios
from app.seed import seed_data

# Importar modelos para que SQLAlchemy los registre en Base
# (Necesario para que create_all() cree las tablas)
from app.modelos import (  # noqa: F401
    articulo,
    intercambio,
    rol,
    usuario,
)


def crear_app() -> FastAPI:
    """
    Crea y configura la instancia de FastAPI con middleware, tablas y rutas.
    
    Returns:
        FastAPI: Aplicación configurada lista para ejecutar
    """
    # Crear instancia de FastAPI con título del proyecto
    app = FastAPI(title=settings.PROJECT_NAME)

    # =================================================================
    # MIDDLEWARE CORS
    # =================================================================
    # Permite que el frontend (Angular) haga peticiones al API
    # allow_origins: URLs autorizadas (desde config.py)
    # allow_credentials: Acepta cookies/headers de autenticación
    # allow_methods: Acepta GET, POST, PUT, DELETE, etc.
    # allow_headers: Acepta cualquier header personalizado
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # =================================================================
    # INICIALIZACIÓN DE BASE DE DATOS
    # =================================================================
    # Crea automáticamente todas las tablas al iniciar la app
    # (Si ya existen, no hace nada - idempotente)
    Base.metadata.create_all(bind=engine)

    # =================================================================
    # EVENTO DE STARTUP - Cargar datos iniciales
    # =================================================================
    # Se ejecuta una sola vez cuando arranca la aplicación
    # Inserta usuarios, roles y artículos de prueba en la BD
    @app.on_event("startup")
    def _seed() -> None:
        """Carga datos iniciales en la base de datos."""
        db = SessionLocal()
        try:
            seed_data(db)
        finally:
            db.close()

    # =================================================================
    # REGISTRO DE ROUTERS (Endpoints)
    # =================================================================
    # Incluye los routers de cada módulo
    # Cada router tiene sus propios prefijos y tags
    app.include_router(auth.router)          # /auth - Login, registro
    app.include_router(usuarios.router)      # /usuarios - Perfil
    app.include_router(articulos.router)     # /articulos - CRUD artículos
    app.include_router(intercambios.router)  # /intercambios - CRUD intercambios

    return app


# Crear instancia global de la app
app = crear_app()
