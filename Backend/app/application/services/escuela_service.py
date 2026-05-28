#Esto es lo que el usuario va a utilizar

from app.domain.models.escuela import Escuela
from app.domain.ports.escuela_repository import EscuelaRepository
from app.adapters.api.schemas import EscuelaUpdate
from fastapi import HTTPException

class EscuelaService:
    
    def __init__(self,repository:EscuelaRepository):
        self.repository=repository
        
    def agregar_escuela(self, nombre: str, ubicacion: str, nivel_academico: str, telefono: str,id_usuario:int) -> dict:
        resultado=self.repository.obtener_por_usuario(id_usuario)
        if resultado is not None:
            raise HTTPException(status_code=400, detail=f"Solo puede estar asociado 1 escuela por usuario, ustdes ya se encuentra asociado a {resultado.nombre}.")

        if len(telefono)<10:
            raise HTTPException(status_code=400, detail=f"La escuela debe tener un número de telefono valido.")
        
        escuela = Escuela(
            id_escuela=None,
            id_usuario=id_usuario,
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
        if "telefono" in datos_dict and len(datos_dict["telefono"]) < 10:
            raise HTTPException(status_code=400, detail="La escuela debe tener un número de telefono valido.")
        
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
    
    def obtener_por_usuario(self, id_usuario:int) -> Escuela:
        resultado=self.repository.obtener_por_usuario(id_usuario)
        if resultado is None:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado
