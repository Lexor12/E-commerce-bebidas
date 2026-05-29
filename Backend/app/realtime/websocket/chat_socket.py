import json
from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Query
from app.application.services.chat_service import ChatService
from app.adapters.dependencies.container import  get_faq_service, get_mensaje_repo
from app.adapters.dependencies.auth_dependency import verify_token_ws
from app.infrastructure.auth.jwt_service import JWTService

router = APIRouter()

class ConnectionManager:
    
    def __init__(self):
        self.active_connections:dict ={}# { id_usuario: websocket }
        
    async def connect(self,id_usuario:int,websocket: WebSocket):
        await websocket.accept()
        self.active_connections[id_usuario]=websocket
        
    def disconnect(self, id_usuario: int):
        if id_usuario in self.active_connections:
            del self.active_connections[id_usuario]
            
    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))
        
manager = ConnectionManager()

@router.websocket("/ws/chat")#No podemos usar directamente get_current_user, ya que no se puede implementar Depends en un websocket
async def websocket_endpoint(websocket:WebSocket,token:str=Query(...)):#Si o si debe ser query, esto no permite body
    user=verify_token_ws(token)
    if user is None:
        await websocket.close(code=1008)
        return
    id_usuario = int(user["id"])
    username=user["username"]
    
    await manager.connect(id_usuario,websocket)
    
    chat_service = ChatService(get_faq_service(),get_mensaje_repo())
    await manager.send_message({
        "de": "bot",
        "contenido": f"¡Hola {username}! 👋 ¿En qué puedo ayudarte hoy?",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    },websocket)
    try:
        while True:
            data=await websocket.receive_text()
            respuesta=chat_service.process_message(id_usuario,data)
            await manager.send_message(respuesta,websocket)
    except WebSocketDisconnect:
        manager.disconnect(id_usuario)