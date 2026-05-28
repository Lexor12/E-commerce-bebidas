from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer  # ← CAMBIA
from app.adapters.dependencies.container import get_jwt_service, get_user_repo,get_refresh_repo
from app.application.services.auth_service import AuthService

#security = HTTPBearer()#le dice a FastAPI 
#que espere un token en el header 
# Authorization: Bearer .... 
# Si no viene el header, FastAPI rechaza solo antes de llegar a tu código

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#le dice a FastAPI dónde está el endpoint de login. 
# Swagger usa esto para mostrar el botón Authorize con 
# un formulario de username/password en lugar de solo 
# pedir el token crudo.

def get_current_user(
    token: str = Depends(oauth2_scheme),  #ahora el token llega directo como string
    jwt = Depends(get_jwt_service),
    user_repo = Depends(get_user_repo),
    refresh_repo=Depends(get_refresh_repo)
):
    service = AuthService(jwt, user_repo,refresh_repo)
    try:
        payload = service.verify(token)#credentials.credentials — es el token en sí, el string 
        return {
                "id": payload["sub"],
                "username": payload["username"],
                "rol": payload["rol"]
            }#Retorna de los datos del token ya decodificados
    except:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
def     require_rol(rol: str):
    def verificar(user=Depends(get_current_user)):
        if user["rol"] != rol:
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return user
    return verificar