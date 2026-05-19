
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SolicitudSalida(BaseModel):
    id: int
    articulo_id: int
    solicitante_id: int
    mensaje: Optional[str] = None
    estado: str
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
