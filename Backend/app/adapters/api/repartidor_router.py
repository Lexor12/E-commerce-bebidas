from fastapi import APIRouter
from app.application.services.repartidor_service import RepartidorService
from app.infrastructure.db.supabase.repartidor_repository_supabase import SupabaseRepartidorRepository
from app.adapters.api.schemas import RepartidorCreate, RepartidorUpdate

router = APIRouter()

repo=SupabaseRepartidorRepository()
service=RepartidorService(repo)

@router.post("/repartidor")
def create_repartidor(body:RepartidorCreate):
    return service.agregar_repartidor(
            nombre=        body.nombre,
            fecha_ingreso= body.fecha_ingreso,
            calificacion=  body.calificacion,
            telefono=      body.telefono
        )

@router.patch("/repartidor/{id_repartidor}")
def editar_repartidor(id_repartidor:int,body:RepartidorUpdate):
    return service.editar_repartidor(id_repartidor=id_repartidor,datos=body)

@router.get("/repartidor/{id_repartidor}")
def ver_repartidor(id_repartidor:int):
    return service.ver_repartidor(id_repartidor=id_repartidor)

@router.get("/repartidor")
def ver_repartidores():
    return service.ver_repartidores()

@router.delete("/repartidor/{id_repartidor}")
def desactivar_repartidor(id_repartidor:int):
    return service.desactivar_repartidor(id_repartidor=id_repartidor)

@router.patch("/repartidor/{id_repartidor}/activar")
def activar_repartidor(id_repartidor:int):
    return service.activar_repartidor(id_repartidor=id_repartidor)