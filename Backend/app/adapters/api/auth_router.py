from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # ← NUEVO
from app.application.services.auth_service import AuthService
from app.adapters.api.schemas import UsuarioCreate,UsuarioRolUpdate,RefreshTokens
from app.adapters.dependencies.container import get_jwt_service, get_user_repo,get_refresh_repo
from app.adapters.dependencies.auth_dependency import require_rol
router = APIRouter(prefix="/auth")

@router.post("/registrar", tags=["Auth"])
def registrar(body: UsuarioCreate, jwt=Depends(get_jwt_service), user_repo=Depends(get_user_repo), refresh_repo=Depends(get_refresh_repo)):
    service = AuthService(jwt, user_repo, refresh_repo)
    try:
        return service.registrar(body.username, body.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", tags=["Auth"])
def login(form: OAuth2PasswordRequestForm = Depends(), jwt=Depends(get_jwt_service), user_repo=Depends(get_user_repo), refresh_repo=Depends(get_refresh_repo)):
    service = AuthService(jwt, user_repo, refresh_repo)
    try:
        return service.login(form.username, form.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.patch("/usuario/{id_usuario}/rol", tags=["Auth"])
def cambiar_rol(id_usuario: int, body: UsuarioRolUpdate, user=Depends(require_rol("admin")), jwt=Depends(get_jwt_service), user_repo=Depends(get_user_repo), refresh_repo=Depends(get_refresh_repo)):
    service = AuthService(jwt, user_repo, refresh_repo)
    try:
        return service.cambiar_rol(id_usuario, body.rol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh", tags=["Auth"])
def refresh(refresh_token: RefreshTokens, jwt=Depends(get_jwt_service), user_repo=Depends(get_user_repo), refresh_repo=Depends(get_refresh_repo)):
    service = AuthService(jwt, user_repo, refresh_repo)
    try:
        return service.refresh(refresh_token.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout", tags=["Auth"])
def logout(refresh_token: RefreshTokens, jwt=Depends(get_jwt_service), user_repo=Depends(get_user_repo), refresh_repo=Depends(get_refresh_repo)):
    service = AuthService(jwt, user_repo, refresh_repo)
    try:
        return service.logout(refresh_token.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))