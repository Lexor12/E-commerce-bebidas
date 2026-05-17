from fastapi import APIRouter
from app.application.services.pedido_service import PedidoService
from app.infrastructure.db.supabase.pedido_repository_supabase import SupabasePedidoRepository
from app.adapters.api.schemas import PedidoCreate

router = APIRouter()

repo=SupabasePedidoRepository()
service=PedidoService(repo)

@router.post("/pedido")
def create_pedido(body:PedidoCreate):
    return service.agregar_pedido(
            id_bebida=body.id_bebida,
            id_escuela=body.id_escuela,
            id_repartidor=body.id_repartidor,
            modo_entrega=body.modo_entrega,
            metodo_pago=body.metodo_pago,
            cantidad=body.cantidad
        )

@router.get("/pedido/{id_pedido}")
def ver_pedido(id_pedido:int):
    return service.ver_pedido(id_pedido=id_pedido)

@router.get("/pedido")
def ver_pedidos():
    return service.ver_pedidos()
