from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class RefreshToken:
    id_token: Optional[int]
    token:str
    id_usuario:int
    expira:datetime
    activo:bool=True