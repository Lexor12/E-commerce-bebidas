from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User

class UserRepository(ABC):

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def agregar(self, user: User) -> dict:
        pass
    @abstractmethod
    def modificar_por_id(self,id_usuario:int, datos: dict) -> dict:
        pass
    @abstractmethod
    def cambiar_rol(self, id_usuario: int, rol: str) -> dict:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id_usuario: int) -> Optional[User]:
        pass