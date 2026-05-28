from typing import Optional
from app.domain.models.bebida import Bebida
from app.domain.ports.bebida_repository import BebidaRepository
from app.infrastructure.db.supabase.client import engine
from sqlalchemy import Table, Column, Integer,Numeric, Boolean,String, MetaData

metadata= MetaData()

tabla_bebida=Table(
    "Bebida",
    metadata,
    Column("id_bebida",Integer,primary_key=True,autoincrement=True),
    Column("nombre", String),
    Column("marca", String),
    Column("litros", Numeric),
    Column("cantidad", Integer),
    Column("precio", Numeric),
    Column("ingredientes", String),
    Column("advertencias", String),
    Column("estatus", Boolean, default=True) # Mapea tu BOOLEAN
)

#metadata.create_all(engine)

class SupabaseBebidaRepository(BebidaRepository):

    def agregar(self, bebida: Bebida) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_bebida.insert().values(
                nombre=bebida.nombre,
                marca=bebida.marca,
                litros=bebida.litros,
                cantidad=bebida.cantidad,
                precio=bebida.precio,
                ingredientes=bebida.ingredientes,
                advertencias=bebida.advertencias,
                estatus=True
            )
            result=conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1, 
                "mensaje": f"Bebida agregada exitosamente con id {result.inserted_primary_key[0]}"
            }

    def ver_por_id(self, id_bebida: int) -> Optional[Bebida]:
        with engine.connect() as conn:
            sentencia = tabla_bebida.select().where(tabla_bebida.c.id_bebida==id_bebida)
            resultado = conn.execute(sentencia).fetchone()
            #En SQLAlchemy, resultado es un objeto de tipo Row (una clase interna de SQLAlchemy, específicamente sqlalchemy.engine.row.Row).
            # Se comporta como objeto con atributos, como diccionario clave alor o como tupla por indice 
        if resultado is None:
            return None
        # Usamos a resultado por propiedades asi como objeto
        return Bebida(
            id_bebida=resultado.id_bebida,
            nombre=resultado.nombre,
            marca=resultado.marca,
            litros=resultado.litros,
            cantidad=resultado.cantidad,
            precio=resultado.precio,
            ingredientes=resultado.ingredientes,
            advertencias=resultado.advertencias,
            estatus=resultado.estatus
        )
        
    def ver_todos(self) -> list:
        with engine.connect() as conn:
            sentencia = tabla_bebida.select()
            resultados=conn.execute(sentencia).fetchall()
    
        lista = []
        for resultado in resultados:
            bebida = Bebida(
            id_bebida=    resultado.id_bebida,
            nombre=       resultado.nombre,
            marca=        resultado.marca,
            litros=       resultado.litros,
            cantidad=     resultado.cantidad,
            precio=       resultado.precio,
            ingredientes= resultado.ingredientes,
            advertencias= resultado.advertencias,
            estatus=      resultado.estatus
            )
            lista.append(bebida)
            
        return lista

    def editar_por_id(self, id_bebida: int, datos: dict) -> dict:
        with engine.connect() as conn:
            valores_a_actualizar = {k: v for k, v in datos.items() if v is not None}
            if not valores_a_actualizar:
                return {"status": 0, "mensaje": "No se proporcionaron datos para actualizar."}
            
            sentencia=tabla_bebida.update().where(tabla_bebida.c.id_bebida==id_bebida, tabla_bebida.c.estatus==True).values(**valores_a_actualizar)
            resultado = conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount == 0:
                return {"status": 0, "mensaje": "Bebida no encontrada o inactiva."}
            return {"status": 1, "mensaje": "Bebida actualizada correctamente."}

    def desactivar_por_id(self, id_bebida: int) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_bebida.update().where(tabla_bebida.c.id_bebida==id_bebida,tabla_bebida.c.estatus==True).values(estatus=False)
            resultado = conn.execute(sentencia)
            conn.commit()
            
            if resultado.rowcount==0:
                return {"status": 0, "mensaje": "Bebida no encontrada o ya inactiva."}
            return {"status": 1, "mensaje": "Bebida desactivada correctamente."}
    
    def activar_por_id(self, id_bebida: int) -> dict:
        with engine.connect() as conn:
            stmt = tabla_bebida.update().where(tabla_bebida.c.id_bebida == id_bebida, tabla_bebida.c.estatus == False).values(estatus=True)
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                return {"status": 0, "mensaje": "Bebida no encontrada o ya activa."}
            return {"status": 1, "mensaje": "Bebida activada correctamente."}