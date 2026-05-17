# E-commerce-bebidas

1. domain/models/       → tus dataclasses (Escuela, Bebida, etc.)
2. domain/ports/        → las clases ABC con @abstractmethod
3. infrastructure/db/supabase/client.py  → conexión con tu anon key
4. infrastructure/db/supabase/*_supabase.py → implementaciones con .rpc()
5. application/services/  → los services que usan los ports
6. adapters/api/schemas.py → modelos Pydantic (request/response)
7. adapters/api/*_router.py → los endpoints FastAPI
8. main.py              → registra todos los routers