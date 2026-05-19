
from enum import Enum


class EstadoIntercambio(str, Enum):
    pendiente = "pendiente"
    aceptado = "aceptado"
    rechazado = "rechazado"
    completado = "completado"
