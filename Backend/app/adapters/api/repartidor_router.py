from fastapi import APIRouter,Depends
from app.application.services.repartidor_service import RepartidorService
from app.infrastructure.db.supabase.repartidor_repository_supabase import SupabaseRepartidorRepository
from app.adapters.api.schemas import RepartidorCreate, RepartidorUpdate
from app.adapters.dependencies.auth_dependency import get_current_user,require_rol
router = APIRouter()

repo=SupabaseRepartidorRepository()
service=RepartidorService(repo)

@router.post("/repartidor",summary="Crear un repartidor.",
    description="Agrega un nuevo repartidor al sistema.",)
def create_repartidor(body:RepartidorCreate,user=Depends(require_rol("admin"))):
    return service.agregar_repartidor(
            nombre=        body.nombre,
            calificacion=body.calificacion,
            telefono=      body.telefono
        )

@router.patch("/repartidor/{id_repartidor}",summary="Editar un repartidor.",
    description="Actualiza parcialmente los datos de un repartidor existente.",)
def editar_repartidor(id_repartidor:int,body:RepartidorUpdate,user=Depends(require_rol("admin"))):
    return service.editar_repartidor(id_repartidor=id_repartidor,datos=body)

@router.get("/repartidor/{id_repartidor}",summary="Obtener un repartidor.",
    description="Recupera la información detallada de un repartidor específico por su ID.",)
def ver_repartidor(id_repartidor:int,user=Depends(get_current_user)):
    return service.ver_repartidor(id_repartidor=id_repartidor)

@router.get("/repartidor",summary="Listar repartidores.",
    description="Obtiene el listado completo de los repartidores registrados.",)
def ver_repartidores(user=Depends(get_current_user)):
    return service.ver_repartidores()

@router.delete("/repartidor/{id_repartidor}",summary="Desactivar un repartidor (Soft Delete).",
    description="Realiza un borrado lógico (soft delete) desactivando o deshabilitando al repartidor del sistema por su ID sin eliminarlo físicamente.",)
def desactivar_repartidor(id_repartidor:int,user=Depends(require_rol("admin"))):
    return service.desactivar_repartidor(id_repartidor=id_repartidor)

@router.patch("/repartidor/{id_repartidor}/activar",summary="Activar un repartidor.",
    description="Reactiva o habilita nuevamente a un repartidor del sistema por su ID.",)
def activar_repartidor(id_repartidor:int,user=Depends(require_rol("admin"))):
    return service.activar_repartidor(id_repartidor=id_repartidor)