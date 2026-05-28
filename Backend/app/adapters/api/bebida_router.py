from fastapi import APIRouter,Depends
from app.application.services.bebida_service import BebidaService
from app.infrastructure.db.supabase.bebida_repository_supabase import SupabaseBebidaRepository
from app.adapters.api.schemas import BebidaCreate,BebidaUpdate
from app.adapters.dependencies.auth_dependency import require_rol,get_current_user


router = APIRouter()

repo = SupabaseBebidaRepository()
service = BebidaService(repo)

@router.post("/bebida")
def agregar_bebida(body:BebidaCreate,user=Depends(require_rol("admin")),):
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
def editar_bebida(id_bebida:int,body:BebidaUpdate,user=Depends(require_rol("admin"))):
    return service.editar_bebida(id_bebida=id_bebida,datos=body)

@router.get("/bebida/{id_bebida}")
def ver_bebida(id_bebida:int,user=Depends(get_current_user)):
    return service.ver_bebida(id_bebida=id_bebida)

@router.get("/bebida")
def ver_bebidas(user=Depends(get_current_user)):
    return service.ver_bebidas()

@router.delete("/bebida/{id_bebida}")
def desactivar_bebida(id_bebida:int,user=Depends(require_rol("admin"))):
    return service.desactivar_bebida(id_bebida=id_bebida)

@router.patch("/bebida/{id_bebida}/activar")
def activar_bebida(id_bebida:int,user=Depends(require_rol("admin"))):
    return service.activar_bebida(id_bebida=id_bebida)