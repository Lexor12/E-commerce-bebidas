from app.domain.models.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository
from app.domain.ports.bebida_repository import BebidaRepository # Necesario para sacar el precio
from app.domain.ports.escuela_repository import EscuelaRepository # Necesario para sacar el precio
from app.domain.ports.repartidor_repository import RepartidorRepository # Necesario para sacar el precio
from fastapi import HTTPException
from datetime import datetime

class PedidoService:
    def __init__(self,pedido_repository:PedidoRepository,bebida_repository: BebidaRepository,escuela_repository: EscuelaRepository,repartidor_repository: RepartidorRepository):
        self.repository=pedido_repository
        self.bebida_repository=bebida_repository
        self.escuela_repository=escuela_repository
        self.repartidor_repository=repartidor_repository
        
    def agregar_pedido(self,id_bebida: int, id_escuela: int, id_repartidor: int, modo_entrega: str, metodo_pago: str, cantidad: int) -> dict:
        if cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero.")
        
        bebida = self.bebida_repository.ver_por_id(id_bebida)
        if not bebida:
            raise HTTPException(status_code=404, detail="La bebida seleccionada no existe.")
        escuela = self.escuela_repository.ver_por_id(id_escuela)
        if not escuela:
            raise HTTPException(status_code=404, detail="La escuela seleccionada no existe.")
        repartidor = self.repartidor_repository.ver_por_id(id_repartidor)
        if not repartidor:
            raise HTTPException(status_code=404, detail="La repartidor seleccionada no existe.")
        
        if bebida.cantidad<cantidad:
            raise HTTPException(status_code=404, detail="No hay stock.")
        
        cantidadNueva = bebida.cantidad-cantidad
        self.bebida_repository.editar_por_id(bebida.id_bebida,{"cantidad":cantidadNueva})
        precio_actual = float(bebida.precio)
        total_calculado = precio_actual * cantidad
        fecha_actual = datetime.now()
        
        pedido = Pedido(
            id_pedido=None,
            id_bebida=id_bebida,
            id_escuela=id_escuela,
            id_repartidor=id_repartidor,
            fecha_hora=fecha_actual,
            modo_entrega=modo_entrega,
            total=total_calculado,
            precio_unitario=precio_actual,
            metodo_pago=metodo_pago,
            cantidad=cantidad
        )
        
        return self.repository.agregar(pedido=pedido)
    
    def ver_pedido(self,id_pedido:int):
        resultado = self.repository.ver_por_id(id_pedido=id_pedido)
        if resultado is None:
            raise HTTPException(status_code=400,detail=f"El pedido con ID {id_pedido} no existe.")
        return resultado
            
    
    def ver_pedidos(self) -> list:
        return self.repository.ver_todos()