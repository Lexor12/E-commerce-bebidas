from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.bebida import Bebida

class BebidaRepository(ABC):
    @abstractmethod
    def agregar(self, bebida: Bebida) -> dict:
        pass
    @abstractmethod
    def ver_por_id(self, id_bebida: int) -> Optional[Bebida]:
        pass
    
    @abstractmethod
    def ver_todos(self) -> list:
        pass
    
    @abstractmethod
    def editar_por_id(self, id_bebida: int, datos: dict) -> dict:
        pass
    @abstractmethod
    def desactivar_por_id(self, id_bebida: int) -> dict:
        pass
    @abstractmethod
    def activar_por_id(self, id_bebida: int) -> dict:
        pass