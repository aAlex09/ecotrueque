
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistorialSalida(BaseModel):
    id: int
    usuario_id: int
    titulo: str
    detalle: Optional[str] = None
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
