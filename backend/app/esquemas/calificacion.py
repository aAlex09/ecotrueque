
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CalificacionSalida(BaseModel):
    id: int
    emisor_id: int
    receptor_id: int
    puntaje: int
    comentario: Optional[str] = None
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
