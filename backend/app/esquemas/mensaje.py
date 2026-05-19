
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MensajeSalida(BaseModel):
    id: int
    emisor_id: int
    receptor_id: int
    contenido: str
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
