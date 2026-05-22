from fastapi import APIRouter
from app.application.services.pedido_service import PedidoService
from app.infrastructure.db.supabase.pedido_repository_supabase import SupabasePedidoRepository
from app.infrastructure.db.supabase.bebida_repository_supabase import SupabaseBebidaRepository
from app.infrastructure.db.supabase.escuela_repository_supabase import SupabaseEscuelaRepository
from app.infrastructure.db.supabase.repartidor_repository_supabase import SupabaseRepartidorRepository
from app.adapters.api.schemas import PedidoCreate

router = APIRouter()

repo=SupabasePedidoRepository()
repo_bebida=SupabaseBebidaRepository()
repo_escuela=SupabaseEscuelaRepository()
repo_repartidor=SupabaseRepartidorRepository()
service=PedidoService(repo,repo_bebida,repo_escuela,repo_repartidor)

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
