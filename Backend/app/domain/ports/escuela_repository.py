from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.escuela import Escuela

class EscuelaRepository(ABC): #Heredamos de ABC para permitir clases abstractas
    @abstractmethod
    def agregar(self,escuela:Escuela) -> dict:
        pass
    
    @abstractmethod
    def obtener_por_usuario(self, id_usuario:int) -> Optional[Escuela]:
        pass
    @abstractmethod
    def ver_por_id(self,id_escuela:int) ->Optional[Escuela]:
        pass #Ponemos optional, ya que como puede retornar None, es vital en caso de que se busque un objeto no existente
    
    @abstractmethod
    def ver_todos(self) ->list:
        pass #Ponemos optional, ya que como puede retornar None, es vital en caso de que se busque un objeto no existente
    @abstractmethod
    def editar_por_id(self,id_escuela:int,datos:dict)->dict:
        pass # el pass es fundamental para que digamos que "aqui no se hace nada, pasa a la siguiente declaracion" *la que si sobreescribe esta que implementa la clase*
    @abstractmethod
    def desactivar_por_id(self,id_escuela:int)->dict:
        pass
    @abstractmethod
    def activar_por_id(self,id_escuela:int)->dict:
        pass
    