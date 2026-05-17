#Esto es lo que el usuario va a utilizar

from app.domain.models.escuela import Escuela
from app.domain.ports.escuela_repository import EscuelaRepository
from app.adapters.api.schemas import EscuelaUpdate

class EscuelaService:
    
    def __init__(self,repository:EscuelaRepository):
        self.repository=repository
        
    def agregar_escuela(self, nombre: str, ubicacion: str, nivel_academico: str, telefono: str) -> str:
        escuela = Escuela(
            id_escuela=None,
            nombre=nombre,
            ubicacion=ubicacion,
            nivel_academico=nivel_academico,
            telefono=telefono
        )
        return self.repository.agregar(escuela=escuela)
    
    def ver_escuela(self,id_escuela:int):
        return self.repository.ver_por_id(id_escuela=id_escuela)
    
    def ver_escuelas(self) -> list:
        return self.repository.ver_todos()
    
    def editar_escuela(self,id_escuela:int,datos:EscuelaUpdate) ->str:
        return self.repository.editar_por_id(id_escuela=id_escuela,datos=datos)
    def desactivar_escuela(self,id_escuela:int) ->dict:
        return self.repository.desactivar_por_id(id_escuela=id_escuela)
    def activar_escuela(self,id_escuela:int) ->dict:
        return self.repository.activar_por_id(id_escuela=id_escuela)