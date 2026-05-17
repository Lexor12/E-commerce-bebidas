from app.domain.models.bebida import Bebida
from app.domain.ports.bebida_repository import BebidaRepository
from app.adapters.api.schemas import BebidaUpdate

class BebidaService:
    def __init__(self, repository: BebidaRepository):
        self.repository = repository
    def agregar_bebida(self, nombre: str, marca: str, litros: int, cantidad: int, precio: float, ingredientes: str, advertencias: str) -> str:
        bebida = Bebida(
            id_bebida=None,
            nombre=nombre,
            marca=marca,
            litros=litros,
            cantidad=cantidad,
            precio=precio,
            ingredientes=ingredientes,
            advertencias=advertencias
        )
        return self.repository.agregar(bebida)

    def ver_bebida(self, id_bebida: int):
        return self.repository.ver_por_id(id_bebida)
    
    def ver_bebidas(self) -> list:
        return self.repository.ver_todos()

    def editar_bebida(self, id_bebida: int, datos: BebidaUpdate) -> str:
        return self.repository.editar_por_id(id_bebida, datos)

    def desactivar_bebida(self, id_bebida: int) -> dict:
        return self.repository.desactivar_por_id(id_bebida)
    def activar_bebida(self, id_bebida: int) -> dict:
        return self.repository.activar_por_id(id_bebida)