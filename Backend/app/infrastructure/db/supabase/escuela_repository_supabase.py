from typing import Optional
from app.domain.models.escuela import Escuela
from app.domain.ports.escuela_repository import EscuelaRepository
from app.infrastructure.db.supabase.client import engine
from sqlalchemy import Table, Column, Integer,Numeric, Boolean,String, MetaData

metadata=MetaData()

tabla_escuela = Table(
    "Escuela", metadata,
    Column("id_escuela", Integer, primary_key=True),
    Column("nombre", String),
    Column("ubicacion", String),
    Column("nivel_academico", String),
    Column("telefono", String),
    Column("estatus", Boolean,default=True)
)

metadata.create_all(engine)

class SupabaseEscuelaRepository(EscuelaRepository):
    def agregar(self, escuela:Escuela) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_escuela.insert().values(
                nombre=escuela.nombre,
                ubicacion=escuela.ubicacion,
                nivel_academico=escuela.nivel_academico,
                telefono=escuela.telefono,
                estatus=True
            )
            result = conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1,
                "mensaje": f"Escuela agregada exitosamente con id {result.inserted_primary_key[0]}"
            }
    
    def ver_por_id(self, id_escuela:int) -> Optional[Escuela]:
        with engine.connect() as conn:
            sentencia = tabla_escuela.select().where(tabla_escuela.c.id_escuela==id_escuela)
            resultado=conn.execute(sentencia).fetchone()
        
        if(resultado is None):
            return None
        
        return Escuela(
            id_escuela=resultado.id_escuela,
            nombre=resultado.nombre,
            ubicacion=resultado.ubicacion,
            nivel_academico=resultado.nivel_academico,
            telefono=resultado.telefono,
            estatus=resultado.estatus
        )
    
    def ver_todos(self) -> list:
        with engine.connect() as conn:
            sentencia = tabla_escuela.select()
            resultados=conn.execute(sentencia).fetchall()
        lista=[]
        for resultado in resultados:
            escuela = Escuela(
                id_escuela=resultado.id_escuela,
                nombre=resultado.nombre,
                ubicacion=resultado.ubicacion,
                nivel_academico=resultado.nivel_academico,
                telefono=resultado.telefono,
                estatus=resultado.estatus
            )
            lista.append(escuela)
            
        return lista
        
    
    def editar_por_id(self, id_escuela:int, datos:dict) ->dict:
        with engine.connect() as conn:
            valores_a_actualizar = {k: v for k, v in datos.items() if v is not None}
            if not valores_a_actualizar:
                return {"status": 0, "mensaje": "No se proporcionaron datos para actualizar."}
            
            sentencia=tabla_escuela.update().where(tabla_escuela.c.id_escuela==id_escuela, tabla_escuela.c.estatus==True).values(**valores_a_actualizar)
            resultado = conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount == 0:
                return {"status": 0, "mensaje": "Escuela no encontrada o inactiva."}
            return {"status": 1, "mensaje": "Escuela actualizada correctamente."}
    
    def desactivar_por_id(self, id_escuela: int) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_escuela.update().where(tabla_escuela.c.id_escuela==id_escuela,tabla_escuela.c.estatus==True).values(estatus=False)
            resultado = conn.execute(sentencia)
            conn.commit()
            
            if resultado.rowcount==0:
                return {"status": 0, "mensaje": "Escuela no encontrada o ya inactiva."}
            return {"status": 1, "mensaje": "Escuela desactivada correctamente."}
    
    def activar_por_id(self, id_escuela: int) -> dict:
        with engine.connect() as conn:
            stmt = tabla_escuela.update().where(tabla_escuela.c.id_escuela == id_escuela, tabla_escuela.c.estatus == False).values(estatus=True)
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                return {"status": 0, "mensaje": "Escuela no encontrada o ya activa."}
            return {"status": 1, "mensaje": "Escuela activada correctamente."}