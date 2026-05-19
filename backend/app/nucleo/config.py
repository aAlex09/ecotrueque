"""
=============================================================================
CONFIGURACIÓN
=============================================================================

Settings cargados desde variables de entorno (.env):
- DATABASE_URL: Conexión a PostgreSQL
- SECRET_KEY: Clave para firmar JWT tokens
- ALGORITHM: Algoritmo de cifrado JWT
- ACCESS_TOKEN_EXPIRE_MINUTES: Expiración de tokens en minutos
- CORS_ORIGINS: URLs permitidas para CORS
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración principal cargada desde .env."""

    # =================================================================
    # PROYECTO
    # =================================================================
    PROJECT_NAME: str = "EcoTrueque"  # Nombre de la aplicación

    # =================================================================
    # BASE DE DATOS
    # =================================================================
    # URL de conexión a PostgreSQL (formato: postgresql://usuario:pass@host:puerto/bd)
    DATABASE_URL: str

    # =================================================================
    # SEGURIDAD - JWT
    # =================================================================
    SECRET_KEY: str  # Clave secreta para firmar tokens JWT (generar aleatoria)
    ALGORITHM: str = "HS256"  # Algoritmo de cifrado (estándar)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Token expira en 60 minutos

    # =================================================================
    # CORS
    # =================================================================
    # URLs permitidas (separadas por comas): "http://localhost:4200,http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:4200"

    # Cargar configuración desde archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte string de CORS_ORIGINS en lista de URLs."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


# Instancia global de settings (se carga al iniciar)
settings = Settings()
