from fastapi import FastAPI
from app.adapters.api.escuela_router import router as escuela_router
from app.adapters.api.repartidor_router import router as repartidor_router
from app.adapters.api.bebida_router import router as bebida_router
from app.adapters.api.pedido_router import router as pedido_router

app = FastAPI(title="E-commerce Bebidas",description="API para gestión de pedidos de bebidas",version="1.0.0")

app.include_router(escuela_router)
app.include_router(repartidor_router)
app.include_router(bebida_router)
app.include_router(pedido_router)