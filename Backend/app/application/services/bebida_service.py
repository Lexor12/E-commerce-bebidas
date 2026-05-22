from app.domain.models.bebida import Bebida
from app.domain.ports.bebida_repository import BebidaRepository
from app.adapters.api.schemas import BebidaUpdate
from fastapi import HTTPException

class BebidaService:
    def __init__(self, repository: BebidaRepository):
        self.repository = repository
    def agregar_bebida(self, nombre: str, marca: str, litros: int, cantidad: int, precio: float, ingredientes: str, advertencias: str) -> dict:
        # CASO DE USO: Crear una entidad nueva en el sistema
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

    def ver_bebida(self, id_bebida: int) -> Bebida:
        bebida= self.repository.ver_por_id(id_bebida)
        if bebida is None:
            raise HTTPException(status_code=404, detail=f"La bebida con ID {id_bebida} no existe.")
        return bebida #caso contrario donde si existe
    
    def ver_bebidas(self) -> list:
        return self.repository.ver_todos()

    def editar_bebida(self, id_bebida: int, datos: BebidaUpdate) -> dict:
        datos_dict = datos.dict(exclude_unset=True)
        resultado = self.repository.editar_por_id(id_bebida, datos_dict)
        if resultado["status"] == 0:
            raise HTTPException(status_code=404, detail=resultado["mensaje"])
        return resultado

    def desactivar_bebida(self, id_bebida: int) -> dict:
        resultado= self.repository.desactivar_por_id(id_bebida)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado
    
    def activar_bebida(self, id_bebida: int) -> dict:
        resultado = self.repository.activar_por_id(id_bebida)
        if resultado["status"] == 0:
            raise HTTPException(status_code=400, detail=resultado["mensaje"])
        return resultado