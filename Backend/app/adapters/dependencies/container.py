from app.infrastructure.auth.jwt_service import JWTService
from app.infrastructure.db.supabase.user_repository_supabase import SupabaseUserRepository
from app.infrastructure.db.supabase.refresh_token_repository_supabase import SupabaseRefreshTokenRepository

def get_jwt_service():
    return JWTService()

def get_user_repo():
    return SupabaseUserRepository()

def get_refresh_repo():  # ← NUEVO
    return SupabaseRefreshTokenRepository()

""" 
Esto, solventa el problema de que por ejemplo, un archivo usa:
repo = SupabaseBebidaRepository()
service = BebidaService(repo)

o sea requiere definir ahi el tipo, y si imaginemonos que tenemos otros archivos
pues cada uno implementa esto, y exite el riesgo de un cambio
y cuando esto ocurra pum, todos deben modificar, pero al usar esto
tipo "aislado", solo modificamos esta funcion y yap
"""