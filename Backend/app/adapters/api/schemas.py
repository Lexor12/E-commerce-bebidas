from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Escuela
class EscuelaCreate(BaseModel):
    nombre: str = Field(...,example="Tecnológico de Monterrey")
    ubicacion: str = Field(...,example="Monterrey")
    nivel_academico:str=Field(...,example="Universidad")
    telefono:str=Field(...,example="3312345678")
    
class EscuelaUpdate(BaseModel):
    nombre: Optional[str] = Field(None,example="Tecnológico de Monterrey")
    ubicacion: Optional[str] = Field(None,example="Monterrey")
    nivel_academico:Optional[str]=Field(None,example="Universidad")
    telefono:Optional[str]=Field(None,example="3312345678")

# Repartidor
class RepartidorCreate(BaseModel):
    nombre:str = Field(..., example="Carlos López")
    calificacion: float= Field(..., example=4.8)
    telefono: str = Field(..., example="3387654321")
    
class RepartidorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, example="Carlos López")
    calificacion: Optional[float] = Field(None, example=4.8)
    telefono: Optional[str] = Field(None, example="3387654321")
    
# Bebida
class BebidaCreate(BaseModel):
    nombre:str=Field(...,example="Agua Mineral")
    marca:str=Field(...,example="Peñafiel")
    litros:float=Field(...,example=1.5)
    cantidad: int = Field(...,example=50)
    precio: float = Field(...,example=18.50)
    ingredientes: str= Field(...,example="Agua, CO2")
    advertencias: str= Field(...,example="Ninguna")
class BebidaUpdate(BaseModel):
    nombre:Optional[str]=Field(None,example="Agua Mineral")
    marca:Optional[str]=Field(None,example="Peñafiel")
    litros:Optional[float]=Field(None,example=1.5)
    cantidad: Optional[int] = Field(None,example=50)
    precio: Optional[float] = Field(None,example=18.50)
    ingredientes: Optional[str]= Field(None,example="Agua, CO2")
    advertencias: Optional[str]= Field(None,example="Ninguna")
    
# Pedido
class PedidoCreate(BaseModel):
    id_bebida:int=Field(...,example=1)
    id_repartidor: int= Field(...,example=1)
    modo_entrega: str= Field(...,example="domicilio")
    metodo_pago:str= Field(...,example="efectivo")
    cantidad:int= Field(...,example=2)
    
# Usuario
class UsuarioCreate(BaseModel):
    username: str
    password: str
    
class UsuarioRolUpdate(BaseModel):
    rol: str = Field(..., example="cliente")
    
class RefreshTokens(BaseModel):
    refresh_token: str = Field(...)