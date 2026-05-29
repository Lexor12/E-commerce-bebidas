from typing import Optional
from app.domain.models.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository
from app.infrastructure.db.supabase.client import engine
from app.infrastructure.db.supabase.tables import tabla_pedido


class SupabasePedidoRepository(PedidoRepository):

    def agregar(self, pedido: Pedido) -> dict:
        with engine.connect() as conn:
            sentencia = tabla_pedido.insert().values(
                id_bebida=pedido.id_bebida,
                id_escuela=pedido.id_escuela,
                id_repartidor=pedido.id_repartidor,
                fecha_hora=pedido.fecha_hora,       # Se guarda lo que calculó el servicio
                modo_entrega=pedido.modo_entrega,
                total=pedido.total,                 # Se guarda lo que calculó el servicio
                precio_unitario=pedido.precio_unitario, # Se guarda lo que calculó el servicio
                metodo_pago=pedido.metodo_pago,
                cantidad=pedido.cantidad
            )
            resultado = conn.execute(sentencia)
            conn.commit()
            return {
                "status": 1, 
                "mensaje": f"Pedido agregado exitosamente con id {resultado.inserted_primary_key[0]}"
            }

    def ver_por_id(self, id_pedido: int) -> Optional[Pedido]:
        with engine.connect() as conn:
            sentencia = tabla_pedido.select().where(tabla_pedido.c.id_pedido == id_pedido)
            resultado = conn.execute(sentencia).fetchone()

        if resultado is None:
            return None

        return Pedido(
            id_pedido=resultado.id_pedido,
            id_bebida=resultado.id_bebida,
            id_escuela=resultado.id_escuela,
            id_repartidor=resultado.id_repartidor,
            fecha_hora=resultado.fecha_hora,
            modo_entrega=resultado.modo_entrega,
            total=float(resultado.total),
            precio_unitario=float(resultado.precio_unitario),
            metodo_pago=resultado.metodo_pago,
            cantidad=resultado.cantidad
        )
        
    def ver_todos(self):
        with engine.connect() as conn:
            sentencia = tabla_pedido.select()
            resultados = conn.execute(sentencia).fetchall()
            
        lista=[]
        for resultado in resultados:
            pedido = Pedido(
                id_pedido=resultado.id_pedido,
                id_bebida=resultado.id_bebida,
                id_escuela=resultado.id_escuela,
                id_repartidor=resultado.id_repartidor,
                fecha_hora=resultado.fecha_hora,
                modo_entrega=resultado.modo_entrega,
                total=float(resultado.total),
                precio_unitario=float(resultado.precio_unitario),
                metodo_pago=resultado.metodo_pago,
                cantidad=resultado.cantidad
            )
            lista.append(pedido)
        return lista