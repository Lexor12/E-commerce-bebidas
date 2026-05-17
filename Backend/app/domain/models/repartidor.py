from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Repartidor:
    id_repartidor: Optional[int]
    nombre: str
    fecha_ingreso: datetime #es el tipo que permite manipular fechas, es como Date de JS
    calificacion: float
    telefono: str
    estatus: bool = True    
