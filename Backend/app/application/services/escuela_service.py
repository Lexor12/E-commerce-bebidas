#Esto es lo que el usuario va a utilizar

from app.domain.models.escuela import Escuela
from app.domain.ports.escuela_repository import EscuelaRepository
from app.adapters.api.schemas import EscuelaUpdate
from fastapi import HTTPException

class EscuelaService:
    
    def __init__(self,repository:EscuelaRepository):
        self.repository=repository
        
    def agregar_escuela(self, nombre: str, ubicacion: str, nivel_academico: str, telefono: str) -> dict:
        escuela = Escuela(
            id_escuela=None,
            nombre=nombre,
            ubicacion=ubicacion,
            nivel_academico=nivel_academico,
            telefono=telefono,
            estatus=True
        )
        return self.repository.agregar(escuela=escuela)
    
    def ver_escuela(self,id_escuela:int) -> Escuela:
        escuela = self.repository.ver_por_id(id_escuela=id_escuela)
        if escuela is None:
            raise HTTPException(status_code=404, detail=f"La escuela con ID {id_escuela} no existe.")
        return escuela #caso contrario donde si existe
    
    def ver_escuelas(self) -> list:
        return self.repository.ver_todos()
    
    def editar_escuela(self,id_escuela:int,datos:EscuelaUpdate) ->dict:
        datos_dict = datos.dict(exclude_unset=True)
        resultado= self.repository.editar_por_id(id_escuela=id_escuela,datos=datos_dict)
        if resultado["status"] == 0:
            raise HTTPException(status_code=404, detail=resultado["mensaje"])
        return resultado
    
    def desactivar_escuela(self,id_escuela:int) ->dict:
        resultado= self.repository.desactivar_por_id(id_escuela=id_escuela)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado
    
    def activar_escuela(self,id_escuela:int) ->dict:
        resultado= self.repository.activar_por_id(id_escuela=id_escuela)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado