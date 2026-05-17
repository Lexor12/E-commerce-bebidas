from datetime import datetime
from app.domain.models.repartidor import Repartidor
from app.domain.ports.repartidor_repository import RepartidorRepository
from app.adapters.api.schemas import RepartidorUpdate

class RepartidorService:

    def __init__(self, repository: RepartidorRepository):
        self.repository = repository

    def agregar_repartidor(self, nombre: str, fecha_ingreso: datetime, calificacion: float, telefono: str) -> str:
        repartidor = Repartidor(
            id_repartidor=None,
            nombre=nombre,
            fecha_ingreso=fecha_ingreso,
            calificacion=calificacion,
            telefono=telefono
        )
        return self.repository.agregar(repartidor)

    def ver_repartidor(self, id_repartidor: int):
        return self.repository.ver_por_id(id_repartidor)
    
    def ver_repartidores(self) -> list:
        return self.repository.ver_todos()

    def editar_repartidor(self, id_repartidor: int, datos: RepartidorUpdate) -> str:
        return self.repository.editar_por_id(id_repartidor, datos)

    def desactivar_repartidor(self, id_repartidor: int) -> dict:
        return self.repository.desactivar_por_id(id_repartidor)
    def activar_repartidor(self, id_repartidor: int) -> dict:
        return self.repository.activar_por_id(id_repartidor)