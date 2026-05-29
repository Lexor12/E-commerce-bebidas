from abc import ABC, abstractmethod
from app.domain.models.mensaje import Mensaje
from typing import Optional

class MensajeRepository(ABC):

    @abstractmethod
    def guardar(self, mensaje: Mensaje) -> dict: 
        pass#cada mensaje del cliente y del bot se guarda en BD.

    @abstractmethod
    def ver_por_usuario(self, id_usuario: int) -> Optional[Mensaje]:
        pass#el cliente puede ver su historial de chat

    @abstractmethod
    def ver_todos(self) -> list:
        pass#el admin puede ver todas las conversaciones desde el backoffice — que es exactamente lo que pide la P4.