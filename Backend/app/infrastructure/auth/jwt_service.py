import os
from jose import jwt, JWTError
from datetime import datetime,timedelta
from app.domain.ports.auth_port import AuthPort
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.environ["SECRET_KEY"]
ALGORITHM =os.environ["ALGORITHM"]
EXPIRE_MINUTES=int(os.environ["EXPIRE_MINUTES"])

class JWTService(AuthPort):
    def create_token(self, data: dict) ->str:
        to_encode = data.copy()#Son los datos, recordando enny del futuro, los JWT, constan de 3 partes, los datos, la firma, y el algoritmo
        expire=datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        to_encode.update({"exp":expire})
        return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload#Automaticamente revisa la fecha, si ya expiro manda error, en caso de que no, pasa los datos
        except JWTError:
            raise Exception("Token inválido")