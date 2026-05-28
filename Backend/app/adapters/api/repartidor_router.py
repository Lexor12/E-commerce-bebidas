from fastapi import APIRouter,Depends
from app.application.services.repartidor_service import RepartidorService
from app.infrastructure.db.supabase.repartidor_repository_supabase import SupabaseRepartidorRepository
from app.adapters.api.schemas import RepartidorCreate, RepartidorUpdate
from app.adapters.dependencies.auth_dependency import get_current_user,require_rol
router = APIRouter()

repo=SupabaseRepartidorRepository()
service=RepartidorService(repo)

@router.post("/repartidor")
def create_repartidor(body:RepartidorCreate,user=Depends(require_rol("admin"))):
    return service.agregar_repartidor(
            nombre=        body.nombre,
            calificacion=body.calificacion,
            telefono=      body.telefono
        )

@router.patch("/repartidor/{id_repartidor}")
def editar_repartidor(id_repartidor:int,body:RepartidorUpdate,user=Depends(require_rol("admin"))):
    return service.editar_repartidor(id_repartidor=id_repartidor,datos=body)

@router.get("/repartidor/{id_repartidor}")
def ver_repartidor(id_repartidor:int):
    return service.ver_repartidor(id_repartidor=id_repartidor)

@router.get("/repartidor")
def ver_repartidores():
    return service.ver_repartidores()

@router.delete("/repartidor/{id_repartidor}")
def desactivar_repartidor(id_repartidor:int,user=Depends(require_rol("admin"))):
    return service.desactivar_repartidor(id_repartidor=id_repartidor)

@router.patch("/repartidor/{id_repartidor}/activar")
def activar_repartidor(id_repartidor:int,user=Depends(require_rol("admin"))):
    return service.activar_repartidor(id_repartidor=id_repartidor)