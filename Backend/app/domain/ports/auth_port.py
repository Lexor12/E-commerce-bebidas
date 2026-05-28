from abc import ABC, abstractmethod

class AuthPort(ABC):

    @abstractmethod
    def create_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass
    
""" 
AuthPort no se llama AuthRepository porque no toca la BD solo genera y verifica tokens. Por eso el nombre es Port a secas.
"""