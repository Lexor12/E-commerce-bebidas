from abc import ABC,abstractmethod
from typing import Optional
from app.domain.models.repartidor import Repartidor

class RepartidorRepository(ABC):
    @abstractmethod
    def agregar(self,repartidor:Repartidor)->dict:
        pass
    @abstractmethod
    def ver_por_id(self,id_repartidor:int)->Optional[Repartidor]:
        pass
    
    @abstractmethod
    def ver_todos(self) -> list:
        pass
    
    @abstractmethod
    def editar_por_id(self, id_repartidor: int, datos: dict) -> dict:
        pass
    @abstractmethod
    def desactivar_por_id(self, id_repartidor: int) -> dict:
        pass
    @abstractmethod
    def activar_por_id(self, id_repartidor: int) -> dict:
        pass