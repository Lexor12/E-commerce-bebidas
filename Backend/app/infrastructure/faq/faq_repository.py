from app.domain.ports.faq_port import FAQPort
from typing import Optional

class FAQMemoryRepository(FAQPort):
    
    FAQS=[    
        {
            "keywords": ["hola", "buenos", "buenas", "saludos", "hey", "buen dia"],
            "respuesta": "¡Hola! 👋 Bienvenido al soporte de E-commerce Bebidas. ¿En qué puedo ayudarte?"
        },
        {
            "keywords": ["precio", "costo", "cuanto", "vale", "cobran", "cuesta"],
            "respuesta": "Los precios de nuestras bebidas varían según marca y presentación. Puedes ver el catálogo completo con precios en la sección de bebidas."
        },
        {
            "keywords": ["bebida", "producto", "catalogo", "disponible", "tienen", "venden", "refresco", "agua", "jugo"],
            "respuesta": "Contamos con un amplio catálogo de bebidas — aguas, refrescos, jugos y más. Consúltalo en la sección de bebidas para ver disponibilidad y precios."
        },
        {
            "keywords": ["pedido", "orden", "estado", "rastrear", "donde esta", "mi compra"],
            "respuesta": "Puedes ver el estado de tu pedido en la sección 'Mis pedidos' dentro de tu cuenta. Si tienes dudas específicas, indícanos tu número de pedido."
        },
        {
            "keywords": ["entrega", "envio", "tiempo", "cuando llega", "demora", "repartidor"],
            "respuesta": "Las entregas se realizan directamente en tu escuela. El tiempo depende de la disponibilidad del repartidor asignado. Puedes ver el detalle en tu pedido."
        },
        {
            "keywords": ["pago", "pagar", "metodo", "efectivo", "tarjeta", "transferencia"],
            "respuesta": "Aceptamos efectivo, tarjeta de débito/crédito y transferencia bancaria. Puedes seleccionar tu método de pago al momento de realizar tu pedido."
        },
        {
            "keywords": ["cancelar", "devolver", "reembolso", "cancelacion"],
            "respuesta": "Los pedidos son registros históricos inmutables. Para gestionar una cancelación o devolución, comunícate con soporte dentro de las 24 horas del pedido."
        },
        {
            "keywords": ["escuela", "registrar", "cuenta", "asociar"],
            "respuesta": "Para realizar pedidos necesitas registrar tu escuela en tu cuenta. Ve a 'Mi escuela' y completa los datos de tu institución."
        },
        {
            "keywords": ["registro", "registrarme", "crear cuenta", "nueva cuenta"],
            "respuesta": "Puedes crear tu cuenta en el botón 'Registrarse'. Solo necesitas un usuario y contraseña. Después podrás asociar tu escuela y hacer pedidos."
        },
        {
            "keywords": ["login", "iniciar sesion", "entrar", "acceder", "contrasena", "password"],
            "respuesta": "Para iniciar sesión usa tu usuario y contraseña registrados. Si olvidaste tu contraseña, contacta a soporte."
        },
        {
            "keywords": ["stock", "inventario", "hay", "quedan", "agotado"],
            "respuesta": "La disponibilidad de cada bebida se muestra en tiempo real en el catálogo. Si una bebida aparece sin stock, puedes consultarnos cuándo se repondrá."
        },
        {
            "keywords": ["horario", "hora", "atienden", "abierto", "servicio"],
            "respuesta": "Nuestro servicio de pedidos está disponible en línea las 24 horas. Las entregas se realizan de lunes a viernes de 8am a 6pm."
        },
        {
            "keywords": ["contacto", "telefono", "correo", "comunicar", "hablar", "soporte", "ayuda", "humano"],
            "respuesta": "Estás chateando con el asistente automático. Si necesitas hablar con un agente, tu mensaje fue enviado y te contactaremos a la brevedad."
        }
    ]
    
    def get_answer(self, question: str) -> Optional[str]:
        question = question.lower()
        mejor_match=None
        mayor_score=0
        
        for faq in self.FAQS:
            score = sum(1 for keyword in faq["keywords"] if keyword in question)
            if score>mayor_score:
                mayor_score=score
                mejor_match=faq["respuesta"]
        
        if mayor_score>0:
            return mejor_match
        return None