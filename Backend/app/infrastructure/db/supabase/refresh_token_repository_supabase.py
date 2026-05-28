from app.domain.models.refresh_token import RefreshToken
from app.domain.ports.refresh_token_repository import RefreshTokenRepository
from app.infrastructure.db.supabase.client import engine
from typing import Optional
from datetime import datetime
from sqlalchemy import Table,Column,String,Boolean,DateTime,MetaData,Integer
import secrets

metadata = MetaData()

tabla_refresh_token=Table(
    "RefreshToken",metadata,
    Column("id_token", Integer, primary_key=True, autoincrement=True),
    Column("token", String),
    Column("id_usuario", Integer),
    Column("expira", DateTime),
    Column("activo", Boolean, default=True)
)

class SupabaseRefreshTokenRepository(RefreshTokenRepository):

    def guardar(self,refresh_token:RefreshToken):
        with engine.connect() as conn:
            sentencia = tabla_refresh_token.insert().values(
                token=refresh_token.token,
                id_usuario=refresh_token.id_usuario,
                expira=refresh_token.expira,
                activo=True
            )
            conn.execute(sentencia)
            conn.commit()
            return {"status": 1, "mensaje": "Refresh token guardado"}
        
    def buscar_por_token(self,token:str)->Optional[RefreshToken]:
        with engine.connect() as conn:
            sentencia = tabla_refresh_token.select().where(
                tabla_refresh_token.c.token == token,
                tabla_refresh_token.c.activo == True
            )
            resultado=conn.execute(sentencia).fetchone()
            if resultado is None:
                return None
            return RefreshToken(
                id_token=resultado.id_token,
                token=resultado.token,
                id_usuario=resultado.id_usuario,
                expira=resultado.expira,
                activo=resultado.activo
            )
            
    def invalidar(self,token:str)->dict:
        with engine.connect() as conn:
            sentencia=tabla_refresh_token.update().where(
                tabla_refresh_token.c.token==token
            ).values(activo=False)
            resultado = conn.execute(sentencia)
            conn.commit()
            if resultado.rowcount==0:
                return {"status": 0, "mensaje": "Token no encontrado"}
            return {"status": 1, "mensaje": "Sesión cerrada correctamente"}