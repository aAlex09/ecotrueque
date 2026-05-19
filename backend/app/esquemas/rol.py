
from pydantic import BaseModel


class RolSalida(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True
