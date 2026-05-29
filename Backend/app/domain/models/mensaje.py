from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Mensaje:
    id_mensaje: Optional[int]
    id_usuario: int #Siempre tiene un usuario asociado
    de: str
    contenido: str
    timestamp: datetime