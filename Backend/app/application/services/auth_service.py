import bcrypt
import secrets
from datetime import timedelta,datetime
from app.domain.ports.refresh_token_repository import RefreshTokenRepository
from app.domain.ports.auth_port import AuthPort
from app.domain.ports.user_repository import UserRepository
from app.domain.models.user import User
from app.domain.models.refresh_token import RefreshToken

class AuthService:
    def __init__(self, auth_provider: AuthPort, user_repo: UserRepository,refresh_token_repo:RefreshTokenRepository):
        self.auth_provider = auth_provider
        self.user_repo = user_repo
        self.refresh_token_repo=refresh_token_repo

    def registrar(self, username: str, password: str) -> dict:
        existente = self.user_repo.buscar_por_username(username)
        if existente is not None:
            raise Exception("El usuario ya existe")

        hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(id=None, username=username, password=hash_password,rol="cliente")
        return self.user_repo.agregar(user)

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.buscar_por_username(username)

        if user is None or not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise Exception("Credenciales inválidas")
        

        access_token= self.auth_provider.create_token({
            "sub":str(user.id),#Este es un identificador unico que no cambia, es mejor usarlo
            "username": username,# Por si acaso, atte kenneth xd
            "rol": user.rol
            })
        
        refresh_token_str = secrets.token_hex(32) #Este genera un string aleatorio
        refresh_token=RefreshToken(
            id_token=None,
            token=refresh_token_str,
            id_usuario=user.id,
            expira=datetime.utcnow()+timedelta(days=7),
            activo=True
        )
        self.refresh_token_repo.guardar(refresh_token)#Creamos el token en la BD, este no guarda datos por si solo, pero es como una garantia que aun podemos crear tokens
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,
            "token_type": "bearer"
        }
        
    def logout(self, refresh_token_str: str) -> dict:
        resultado = self.refresh_token_repo.invalidar(refresh_token_str)
        if resultado["status"] == 0:
            raise Exception("Token no encontrado")
        return {"mensaje": "Sesión cerrada correctamente"}

    def verify(self, token: str) -> dict:
        return self.auth_provider.verify_token(token)
    
    def cambiar_rol(self, id_usuario: int, rol: str) -> dict:
        roles_validos = ["cliente", "admin"]
        if rol not in roles_validos:
            raise Exception(f"Rol inválido, debe ser uno de: {roles_validos}")
        
        usuario = self.user_repo.buscar_por_id(id_usuario)
        if usuario is None:
            raise Exception("Usuario no encontrado")
        
        return self.user_repo.cambiar_rol(id_usuario, rol)
    
    def refresh(self, refresh_token_str: str) -> dict:
        refresh_token = self.refresh_token_repo.buscar_por_token(refresh_token_str)
        if refresh_token is None:
            raise Exception("Refresh token inválido o inactivo")
        if datetime.utcnow() > refresh_token.expira:
            self.refresh_token_repo.invalidar(refresh_token_str)
            raise Exception("Refresh token expirado, inicia sesión de nuevo")
        user = self.user_repo.buscar_por_id(refresh_token.id_usuario)
        if user is None:
            raise Exception("Usuario no encontrado")
        nuevo_access_token = self.auth_provider.create_token({
            "sub": str(user.id),
            "username": user.username,
            "rol": user.rol
        })
        return {
            "access_token": nuevo_access_token,
            "token_type": "bearer"
        }


        
""" 
registrar → hashea la contraseña y guarda en BD
login → busca en BD y compara con bcrypt
verify → delega al puerto, no sabe nada de JWT
"""