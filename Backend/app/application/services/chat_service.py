from datetime import datetime
from app.domain.models.mensaje import Mensaje
from app.domain.ports.faq_port import FAQPort
from app.domain.ports.mensaje_repository import MensajeRepository

class ChatService:
    
    def __init__(self,faq_provider: FAQPort, mensaje_repo: MensajeRepository):
        self.faq_provider=faq_provider
        self.mensaje_repo=mensaje_repo
        
    def process_message(self, id_usuario: int, contenido: str) -> dict:
        try:  
            mensaje_cliente = Mensaje(
                id_mensaje=None,
                id_usuario=id_usuario,
                de="cliente",
                contenido=contenido,
                timestamp=datetime.utcnow()
            )
            self.mensaje_repo.guardar(mensaje_cliente)

            respuesta = self.faq_provider.get_answer(contenido)
        except:
            pass  # el historial falla pero el chat sigue vivo
    # Buscar respuesta
        respuesta = self.faq_provider.get_answer(contenido)

        if respuesta is None:
            respuesta = "Tu mensaje fue recibido, pero no se pudo procesar el mensaje."

        mensaje_bot = Mensaje(
            id_mensaje=None,
            id_usuario=id_usuario,
            de="bot",
            contenido=respuesta,
            timestamp=datetime.utcnow()
        )
        self.mensaje_repo.guardar(mensaje_bot)

        return {
            "de": "bot",
            "contenido": respuesta,
            "timestamp": mensaje_bot.timestamp.isoformat()
        }
    def ver_historial(self, id_usuario: int) -> list:
        return self.mensaje_repo.ver_por_usuario(id_usuario)

    def ver_todas_conversaciones(self) -> list:
        return self.mensaje_repo.ver_todos()
        