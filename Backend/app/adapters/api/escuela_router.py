from fastapi import APIRouter,Depends
from app.application.services.escuela_service import EscuelaService
from app.infrastructure.db.supabase.escuela_repository_supabase import SupabaseEscuelaRepository
from app.adapters.api.schemas import EscuelaCreate, EscuelaUpdate
from app.adapters.dependencies.auth_dependency import get_current_user,require_rol
router = APIRouter()

repo=SupabaseEscuelaRepository()
service=EscuelaService(repo)

@router.post("/escuela")
def create_escuela(body:EscuelaCreate,user=Depends(get_current_user)):
    return service.agregar_escuela(nombre=body.nombre,ubicacion=body.ubicacion,nivel_academico=body.nivel_academico,telefono=body.telefono,id_usuario=int(user["id"]))

@router.patch("/escuela/{id_escuela}")
def editar_escuela(id_escuela:int,body:EscuelaUpdate,user=Depends(require_rol("admin"))):
    return service.editar_escuela(id_escuela=id_escuela,datos=body)

@router.get("/escuela/{id_escuela}")
def ver_escuela(id_escuela:int):
    return service.ver_escuela(id_escuela=id_escuela)

@router.get("/escuela")
def ver_escuelas():
    return service.ver_escuelas()

@router.delete("/escuela/{id_escuela}")
def desactivar_escuela(id_escuela:int,user=Depends(require_rol("admin"))):
    return service.desactivar_escuela(id_escuela=id_escuela)

@router.patch("/escuela/{id_escuela}/activar")
def activar_escuela(id_escuela:int,user=Depends(require_rol("admin"))):
    return service.activar_escuela(id_escuela=id_escuela)