from typing import Optional
from app.domain.models.repartidor import Repartidor
from app.domain.ports.repartidor_repository import RepartidorRepository
from app.infrastructure.db.supabase.client import conn
from app.adapters.api.schemas import RepartidorUpdate

class SupabaseRepartidorRepository(RepartidorRepository):
    def agregar(self, repartidor):
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM agregar_repartidor(%s, %s, %s)", (
            repartidor.nombre,
            repartidor.calificacion,
            repartidor.telefono
        ))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]
    
    def ver_por_id(self, id_repartidor: int) -> Optional[Repartidor]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ver_repartidor_por_id(%s)", (id_repartidor,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado is None:
            return None

        return Repartidor(
            id_repartidor= resultado[0],
            nombre=        resultado[1],
            fecha_ingreso= resultado[2],
            calificacion=  resultado[3],
            telefono=      resultado[4],
            estatus=       resultado[5]
        )

    def ver_todos(self):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ver_repartidores()")
        resultados=cursor.fetchall()#Permite obtener todos
        cursor.close()
        
        lista = []
        for resultado in resultados:
            repartidor = Repartidor(
            id_repartidor= resultado[0],
            nombre=        resultado[1],
            fecha_ingreso= resultado[2],
            calificacion=  resultado[3],
            telefono=      resultado[4],
            estatus=       resultado[5]
            )
            lista.append(repartidor)
        return lista

    def editar_por_id(self, id_repartidor: int, datos: RepartidorUpdate) -> str:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM editar_repartidor_por_id(%s, %s, %s, %s)", (
            id_repartidor,
            datos.nombre,
            datos.calificacion,
            datos.telefono
        ))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]

    def desactivar_por_id(self, id_repartidor: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM desactivar_repartidor_por_id(%s)", (id_repartidor,))
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}
    
    def activar_por_id(self, id_repartidor: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activar_repartidor_por_id(%s)", (id_repartidor,))
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}

