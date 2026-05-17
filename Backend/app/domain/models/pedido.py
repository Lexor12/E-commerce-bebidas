from dataclasses import dataclass
from typing import Optional

@dataclass
class Pedido:
    id_pedido: Optional[int]
    id_bebida: int
    id_escuela: int
    id_repartidor: int
    modo_entrega: str
    metodo_pago: str
    cantidad: int