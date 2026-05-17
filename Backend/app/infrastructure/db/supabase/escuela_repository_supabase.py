from typing import Optional
from app.domain.models.escuela import Escuela
from app.domain.ports.escuela_repository import EscuelaRepository
from app.infrastructure.db.supabase.client import conn
from app.adapters.api.schemas import EscuelaUpdate

class SupabaseEscuelaRepository(EscuelaRepository):
    def agregar(self, escuela):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agregar_escuela(%s, %s, %s, %s)",(escuela.nombre,escuela.ubicacion,escuela.nivel_academico,escuela.telefono))
        
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]
    def ver_por_id(self, id_escuela):
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM ver_escuela_por_id(%s)", (id_escuela,))
        resultado=cursor.fetchone()
        cursor.close()
        
        if(resultado is None):
            return None
        
        return Escuela(
            id_escuela=resultado[0],
            nombre=resultado[1],
            ubicacion=resultado[2],
            nivel_academico=resultado[3],
            telefono=resultado[4],
            estatus=resultado[5]
        )
    
    def ver_todos(self):
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM ver_escuelas()")
        resultados=cursor.fetchall()
        cursor.close()
        
        lista=[]
        for resultado in resultados:
            escuela = Escuela(
                id_escuela=resultado[0],
                nombre=resultado[1],
                ubicacion=resultado[2],
                nivel_academico=resultado[3],
                telefono=resultado[4],
                estatus=resultado[5]
            )
            lista.append(escuela)
            
        return lista
        
    
    def editar_por_id(self, id_escuela:int, datos:EscuelaUpdate):
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM editar_escuela_por_id(%s, %s, %s, %s, %s)", (
            id_escuela,
            datos.nombre,
            datos.ubicacion,
            datos.nivel_academico,
            datos.telefono
        ))
        
        resultado=cursor.fetchone()
        cursor.close()
        return resultado[0]
    
    def desactivar_por_id(self, id_escuela: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM desactivar_escuela_por_id(%s)", (id_escuela,))
        
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}
    def activar_por_id(self, id_escuela: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activar_escuela_por_id(%s)", (id_escuela,))
        
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}