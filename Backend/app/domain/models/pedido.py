from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Pedido:
    id_pedido: Optional[int]
    id_bebida: int
    id_escuela: int
    id_repartidor: int
    fecha_hora: datetime  # <--- Agregado
    modo_entrega: str
    total: float         # <--- Agregado (El cálculo matemático se guarda aquí)
    precio_unitario: float # <--- Agregado
    metodo_pago: str
    cantidad: int