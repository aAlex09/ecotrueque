
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificacionSalida(BaseModel):
    id: int
    usuario_id: int
    titulo: str
    cuerpo: str
    leida: bool
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
