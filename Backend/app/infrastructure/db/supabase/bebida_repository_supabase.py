from typing import Optional
from app.domain.models.bebida import Bebida
from app.domain.ports.bebida_repository import BebidaRepository
from app.infrastructure.db.supabase.client import conn
from app.adapters.api.schemas import BebidaUpdate

class SupabaseBebidaRepository(BebidaRepository):

    def agregar(self, bebida: Bebida) -> str:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agregar_bebida(%s, %s, %s, %s, %s, %s, %s)", (
            bebida.nombre,
            bebida.marca,
            bebida.litros,
            bebida.cantidad,
            bebida.precio,
            bebida.ingredientes,
            bebida.advertencias
        ))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]

    def ver_por_id(self, id_bebida: int) -> Optional[Bebida]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ver_bebida_por_id(%s)", (id_bebida,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado is None:
            return None

        return Bebida(
            id_bebida=    resultado[0],
            nombre=       resultado[1],
            marca=        resultado[2],
            litros=       resultado[3],
            cantidad=     resultado[4],
            precio=       resultado[5],
            ingredientes= resultado[6],
            advertencias= resultado[7],
            estatus=      resultado[8]
        )
        
    def ver_todos(self) -> list:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ver_bebidas()")
        resultados=cursor.fetchall()#Permite obtener todos
        cursor.close()
        
        lista = []
        for resultado in resultados:
            bebida = Bebida(
            id_bebida=    resultado[0],
            nombre=       resultado[1],
            marca=        resultado[2],
            litros=       resultado[3],
            cantidad=     resultado[4],
            precio=       resultado[5],
            ingredientes= resultado[6],
            advertencias= resultado[7],
            estatus=      resultado[8]
            )
            lista.append(bebida)
            
        return lista

    def editar_por_id(self, id_bebida: int, datos: BebidaUpdate) -> str:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM editar_bebida_por_id(%s, %s, %s, %s, %s, %s, %s, %s)", (
            id_bebida,
            datos.nombre,
            datos.marca,
            datos.litros,
            datos.cantidad,
            datos.precio,
            datos.ingredientes,
            datos.advertencias
        ))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]

    def desactivar_por_id(self, id_bebida: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM desactivar_bebida_por_id(%s)", (id_bebida,))
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}
    
    def activar_por_id(self, id_bebida: int) -> dict:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activar_bebida_por_id(%s)", (id_bebida,))
        resultado = cursor.fetchone()
        cursor.close()
        return {"status": resultado[0], "mensaje": resultado[1]}