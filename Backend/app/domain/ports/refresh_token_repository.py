from app.domain.models.refresh_token import RefreshToken
from abc import ABC, abstractmethod
from typing import Optional

class RefreshTokenRepository(ABC):
    @abstractmethod
    def guardar(self,refresh_token:RefreshToken):
        pass
    @abstractmethod
    def buscar_por_token(self,token:str)->Optional[RefreshToken]:
        pass
    @abstractmethod 
    def invalidar(self,token:str)->dict:
        pass