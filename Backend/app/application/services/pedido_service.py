from app.domain.models.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository

class PedidoService:
    def __init__(self,repository:PedidoRepository):
        self.repository=repository
        
    def agregar_pedido(self,id_bebida: int, id_escuela: int, id_repartidor: int, modo_entrega: str, metodo_pago: str, cantidad: int) -> str:
        pedido = Pedido(
            id_pedido=None,
            id_bebida=id_bebida,
            id_escuela=id_escuela,
            id_repartidor=id_repartidor,
            modo_entrega=modo_entrega,
            metodo_pago=metodo_pago,
            cantidad=cantidad
        )
        return self.repository.agregar(pedido=pedido)
    
    def ver_pedido(self,id_pedido:int):
        return self.repository.ver_por_id(id_pedido=id_pedido)
    
    def ver_pedidos(self) -> list:
        return self.repository.ver_todos()