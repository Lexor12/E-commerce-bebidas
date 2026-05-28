from datetime import datetime
from app.domain.models.repartidor import Repartidor
from app.domain.ports.repartidor_repository import RepartidorRepository
from app.adapters.api.schemas import RepartidorUpdate
from fastapi import HTTPException

class RepartidorService:

    def __init__(self, repository: RepartidorRepository):
        self.repository = repository

    def agregar_repartidor(self, nombre: str, calificacion: float, telefono: str) -> dict:
        
        if len(telefono)<10:
            raise HTTPException(status_code=400, detail=f"El repartidor debe tener un número de teléfono valido.")
        
        if calificacion<0:
            raise HTTPException(status_code=400, detail=f"El repartidor debe tener una calificación valida.")
        
        
        fecha_actual = datetime.now()
        
        repartidor = Repartidor(
            id_repartidor=None,
            nombre=nombre,
            fecha_ingreso=fecha_actual,
            calificacion=calificacion,
            telefono=telefono
        )
        return self.repository.agregar(repartidor)

    def ver_repartidor(self, id_repartidor: int) -> Repartidor:
        resultado= self.repository.ver_por_id(id_repartidor)
        if resultado is None:
            raise HTTPException(status_code=404, detail=f"El repartidor con ID {id_repartidor} no existe.")
        return resultado #caso contrario donde si existe
    
    def ver_repartidores(self) -> list:
        return self.repository.ver_todos()

    def editar_repartidor(self, id_repartidor: int, datos: RepartidorUpdate) -> dict:
        datos_dict = datos.dict(exclude_unset=True)
        if "telefono" in datos_dict and len(datos_dict["telefono"]) < 10:
            raise HTTPException(status_code=400, detail="El repartidor debe tener un número de teléfono valido.")
        
        if "calificacion" in datos_dict and datos_dict["calificacion"] < 0:
            raise HTTPException(status_code=400, detail="El repartidor debe tener una calificación valida.")
        
        resultado= self.repository.editar_por_id(id_repartidor, datos_dict)
        if resultado["status"] == 0:
            raise HTTPException(status_code=404, detail=resultado["mensaje"])
        return resultado

    def desactivar_repartidor(self, id_repartidor: int) -> dict:
        resultado= self.repository.desactivar_por_id(id_repartidor)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado
    def activar_repartidor(self, id_repartidor: int) -> dict:
        resultado= self.repository.activar_por_id(id_repartidor)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado