from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.pedido import Pedido

class PedidoRepository(ABC):
    @abstractmethod
    def agregar(self,pedido:Pedido)->dict:
        pass
    @abstractmethod
    def ver_por_id(self,id_pedido:int)->Optional[Pedido]:
        pass
    
    @abstractmethod
    def ver_todos(self) -> list:
        pass