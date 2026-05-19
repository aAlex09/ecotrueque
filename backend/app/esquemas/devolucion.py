
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DevolucionSalida(BaseModel):
    id: int
    intercambio_id: int
    motivo: Optional[str] = None
    estado: str
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
