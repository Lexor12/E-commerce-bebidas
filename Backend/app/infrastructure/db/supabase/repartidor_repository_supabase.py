from typing import Optional
from app.domain.models.repartidor import Repartidor
from app.domain.ports.repartidor_repository import RepartidorRepository
from app.infrastructure.db.supabase.client import engine
from sqlalchemy import Table, Column, Integer,Numeric,DateTime, Boolean,String, MetaData

metadata=MetaData()

tabla_repartidor = Table(
    "Repartidor", metadata,
    Column("id_repartidor", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String),
    Column("fecha_ingreso", DateTime),
    Column("calificacion", Numeric),
    Column("telefono", String),
    Column("estatus", Boolean, default=True)
)

metadata.create_all(engine)
class SupabaseRepartidorRepository(RepartidorRepository):
    def agregar(self, repartidor:Repartidor):
        with engine.connect() as conn:
            sentencia = tabla_repartidor.insert().values(
                nombre=repartidor.nombre,
                fecha_ingreso=repartidor.fecha_ingreso,
                calificacion=repartidor.calificacion,
                telefono=repartidor.telefono,
                estatus=repartidor.estatus
            )
            resultado = conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1,
                "mensaje": f"Repartidor agregado exitosamente con id {resultado.inserted_primary_key[0]}"
            }
    
    def ver_por_id(self, id_repartidor: int) -> Optional[Repartidor]:
        with engine.connect() as conn:
            sentencia = tabla_repartidor.select().where(tabla_repartidor.c.id_repartidor == id_repartidor)
            resultado = conn.execute(sentencia).fetchone()

        if resultado is None:
            return None

        return Repartidor(
            id_repartidor=resultado.id_repartidor,
            nombre=resultado.nombre,
            fecha_ingreso=resultado.fecha_ingreso,
            calificacion=float(resultado.calificacion),
            telefono=resultado.telefono,
            estatus=resultado.estatus
        )

    def ver_todos(self):
        with engine.connect() as conn:
            sentencia = tabla_repartidor.select()
            resultados = conn.execute(sentencia).fetchall()
        
        lista = []
        for resultado in resultados:
            repartidor = Repartidor(
                id_repartidor=resultado.id_repartidor,
                nombre=resultado.nombre,
                fecha_ingreso=resultado.fecha_ingreso,
                calificacion=float(resultado.calificacion),
                telefono=resultado.telefono,
                estatus=resultado.estatus
            )
            lista.append(repartidor)
        return lista

    def editar_por_id(self, id_repartidor: int, datos: dict) -> dict:
        with engine.connect() as conn:
            valores_a_actualizar = {k: v for k, v in datos.items() if v is not None}
            sentencia = tabla_repartidor.update().where(tabla_repartidor.c.id_repartidor == id_repartidor).values(**valores_a_actualizar)
            resultado=conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount == 0:
                return {"status": 0, "mensaje": "Repartidor no encontrado o inactivo."}
            return {"status": 1, "mensaje": "Repartidor actualizado correctamente."}

    def desactivar_por_id(self, id_repartidor: int) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_repartidor.update().where(tabla_repartidor.c.id_repartidor==id_repartidor,tabla_repartidor.c.estatus==True).values(estatus=False)
            resultado = conn.execute(sentencia)
            conn.commit()
            
            if resultado.rowcount==0:
                return {"status": 0, "mensaje": "Repartidor no encontrado o ya inactivo."}
            return {"status": 1, "mensaje": "Repartidor desactivado correctamente."}
    
    def activar_por_id(self, id_repartidor: int) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_repartidor.update().where(tabla_repartidor.c.id_repartidor==id_repartidor,tabla_repartidor.c.estatus==False).values(estatus=True)
            resultado = conn.execute(sentencia)
            conn.commit()
            
            if resultado.rowcount==0:
                return {"status": 0, "mensaje": "Repartidor no encontrado o ya activo."}
            return {"status": 1, "mensaje": "Repartidor activado correctamente."}

