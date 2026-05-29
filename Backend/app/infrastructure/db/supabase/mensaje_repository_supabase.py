from typing import Optional
from app.domain.models.mensaje import Mensaje
from app.domain.ports.mensaje_repository import MensajeRepository
from app.infrastructure.db.supabase.client import engine
from app.infrastructure.db.supabase.tables import tabla_mensaje

class SupabaseMensajeRepository(MensajeRepository):
    
    def guardar(self, mensaje: Mensaje) -> dict: 
        with engine.connect() as conn:
            sentencia = tabla_mensaje.insert().values(
                id_usuario=mensaje.id_usuario,  # ← faltaban los valores
                de=mensaje.de,
                contenido=mensaje.contenido,
                timestamp=mensaje.timestamp
            )
            resultado = conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1, 
                "mensaje": f"Mensaje guardado con id {resultado.inserted_primary_key[0]}"
            }

    def ver_por_usuario(self, id_usuario: int) -> list:  # ← devuelve list no Optional[Mensaje]
        with engine.connect() as conn:
            sentencia = tabla_mensaje.select().where(tabla_mensaje.c.id_usuario == id_usuario)
            resultados = conn.execute(sentencia).fetchall()  # ← fetchall no fetchone
        
        lista = []
        for resultado in resultados:
            lista.append(Mensaje(
                id_mensaje=resultado.id_mensaje,
                id_usuario=resultado.id_usuario,
                de=resultado.de,              
                contenido=resultado.contenido,
                timestamp=resultado.timestamp
            ))
        return lista

    def ver_todos(self) -> list:
        with engine.connect() as conn:
            sentencia = tabla_mensaje.select()
            resultados = conn.execute(sentencia).fetchall()
            
        lista = []
        for resultado in resultados:
            lista.append(Mensaje(        
                id_mensaje=resultado.id_mensaje,
                id_usuario=resultado.id_usuario,
                de=resultado.de,         
                contenido=resultado.contenido,
                timestamp=resultado.timestamp
            ))
        return lista