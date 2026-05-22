from fastapi import FastAPI
from app.adapters.api.escuela_router import router as escuela_router
from app.adapters.api.repartidor_router import router as repartidor_router
from app.adapters.api.bebida_router import router as bebida_router
from app.adapters.api.pedido_router import router as pedido_router

app = FastAPI(title="E-commerce Bebidas",description="API para gestión de pedidos de bebidas",version="1.0.0")

# Agregamos el parámetro tags a cada router
app.include_router(escuela_router, tags=["Escuela"])
app.include_router(repartidor_router, tags=["Repartidor"])
app.include_router(bebida_router, tags=["Bebida"])
app.include_router(pedido_router, tags=["Pedido"])

@app.get("/")
def Inicio():
        return{
            "estatus":"Activo",
            "mensaje":"Bienvenido!, gracias por usar la API."
    }
