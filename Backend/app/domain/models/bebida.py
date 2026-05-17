from dataclasses import dataclass
from typing import Optional

@dataclass
class Bebida:
    id_bebida: Optional[int]#Lo mismo que en Escuela, es para que idealmente sepamos que aun no se encuentra en la bd
    nombre: str
    marca: str
    litros: int
    cantidad: int
    precio: float
    ingredientes: str
    advertencias: str
    estatus: bool = True