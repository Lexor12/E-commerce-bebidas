from fastapi import APIRouter
from app.application.services.bebida_service import BebidaService
from app.infrastructure.db.supabase.bebida_repository_supabase import SupabaseBebidaRepository
from app.adapters.api.schemas import BebidaCreate,BebidaUpdate

router = APIRouter()

repo = SupabaseBebidaRepository()
service = BebidaService(repo)

@router.post("/bebida")
def agregar_bebida(body:BebidaCreate):
    return service.agregar_bebida(
        nombre=body.nombre,
        marca=body.marca,
        litros=body.litros,
        cantidad=body.cantidad,
        precio=body.precio,
        ingredientes=body.ingredientes,
        advertencias=body.advertencias
    )
    
@router.patch("/bebida/{id_bebida}")
def editar_bebida(id_bebida:int,body:BebidaUpdate):
    return service.editar_bebida(id_bebida=id_bebida,datos=body)

@router.get("/bebida/{id_bebida}")
def ver_bebida(id_bebida:int):
    return service.ver_bebida(id_bebida=id_bebida)

@router.get("/bebida")
def ver_bebidas():
    return service.ver_bebidas()

@router.delete("/bebida/{id_bebida}")
def desactivar_bebida(id_bebida:int):
    return service.desactivar_bebida(id_bebida=id_bebida)

@router.patch("/bebida/{id_bebida}/activar")
def activar_bebida(id_bebida:int):
    return service.activar_bebida(id_bebida=id_bebida)