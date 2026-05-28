from typing import Optional
from app.domain.models.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.db.supabase.client import engine
from sqlalchemy import Table, Column, Integer,Numeric, Boolean,String, MetaData

metadata=MetaData()

tabla_usuario = Table(
    "Usuario", metadata,
    Column("id_usuario", Integer, primary_key=True,autoincrement=True),
    Column("username", String),
    Column("password", String),
    Column("rol", String)
)

#metadata.create_all(engine)

class SupabaseUserRepository(UserRepository):
    def buscar_por_username(self, username:str)-> Optional[User]:
        with engine.connect() as conn:
            sentencia = tabla_usuario.select().where(tabla_usuario.c.username==username)
            resultado=conn.execute(sentencia).fetchone()
            
        if(resultado is None):
            return None
        
        return User(
            resultado.id_usuario,
            resultado.username,
            resultado.password,
            resultado.rol
        )
    
    def agregar(self, user:User) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_usuario.insert().values(
                username=user.username,
                password=user.password,#Por default somos cliente
                rol=user.rol
            )
            result = conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1,
                "mensaje": f"Usuario agregado exitosamente con id {result.inserted_primary_key[0]}"
            }
            
    def modificar_por_id(self,id_usuario:int, datos: dict)->dict:
        with engine.connect() as conn:
            valores_a_actualizar = {k: v for k, v in datos.items() if v is not None}
            if not valores_a_actualizar:
                return {"status": 0, "mensaje": "No se proporcionaron datos para actualizar."}
            
            sentencia=tabla_usuario.update().where(tabla_usuario.c.id_usuario==id_usuario).values(**valores_a_actualizar)
            resultado = conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount == 0:
                return {"status": 0, "mensaje": "Usuario no encontrado o inactivo."}
            return {"status": 1, "mensaje": "Usuario actualizado correctamente."}
    
    def cambiar_rol(self, id_usuario: int, rol: str) -> dict:
        with engine.connect() as conn:
            sentencia=tabla_usuario.update().where(tabla_usuario.c.id_usuario==id_usuario).values({"rol":rol})
            resultado = conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount == 0:
                return {"status": 0, "mensaje": "Usuario no encontrado o inactivo."}
            return {"status": 1, "mensaje": "Usuario actualizado correctamente."}
    
    def buscar_por_id(self, id_usuario: int) -> Optional[User]:
        with engine.connect() as conn:
            sentencia = tabla_usuario.select().where(tabla_usuario.c.id_usuario==id_usuario)
            resultado = conn.execute(sentencia).fetchone()
            if resultado is None:
                return None
            return User(
                id=resultado.id_usuario,
                username=resultado.username,
                password=resultado.password,
                rol=resultado.rol
            )   