from fastapi import APIRouter,Depends
from app.application.services.bebida_service import BebidaService
from app.infrastructure.db.supabase.bebida_repository_supabase import SupabaseBebidaRepository
from app.adapters.api.schemas import BebidaCreate,BebidaUpdate
from app.adapters.dependencies.auth_dependency import require_rol,get_current_user


router = APIRouter()

repo = SupabaseBebidaRepository()
service = BebidaService(repo)

@router.post("/bebida",summary="Crear una bebida.",
    description="Agrega una bebida al sistema.",)
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
    
@router.patch("/bebida/{id_bebida}",summary="Editar una bebida.",
    description="Actualiza parcialmente los datos de una bebida existente.",)
def editar_bebida(id_bebida:int,body:BebidaUpdate,user=Depends(require_rol("admin"))):
    return service.editar_bebida(id_bebida=id_bebida,datos=body)

@router.get("/bebida/{id_bebida}",summary="Obtener una bebida.",
    description="Recupera la información detallada de una bebida por su ID.",)
def ver_bebida(id_bebida:int):
    return service.ver_bebida(id_bebida=id_bebida)

@router.get("/bebida",summary="Listar bebidas.",
    description="Obtiene el listado completo de las bebidas registradas.",)
def ver_bebidas():
    return service.ver_bebidas()

@router.delete("/bebida/{id_bebida}",summary="Desactivar una bebida (Soft Delete).",
    description="Realiza un borrado lógico (soft delete) desactivando o deshabilitando la bebida del sistema por su ID sin eliminarla físicamente.",)
def desactivar_bebida(id_bebida:int,user=Depends(require_rol("admin"))):
    return service.desactivar_bebida(id_bebida=id_bebida)

@router.patch("/bebida/{id_bebida}/activar",summary="Activar una bebida.",
    description="Reactiva o habilita nuevamente una bebida del sistema por su ID.",)
def activar_bebida(id_bebida:int,user=Depends(require_rol("admin"))):
    return service.activar_bebida(id_bebida=id_bebida)