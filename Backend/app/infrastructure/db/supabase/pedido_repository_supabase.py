from typing import Optional
from app.domain.models.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository
from app.infrastructure.db.supabase.client import conn

class SupabasePedidoRepository(PedidoRepository):

    def agregar(self, pedido: Pedido) -> str:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agregar_pedido(%s, %s, %s, %s, %s, %s)", (
            pedido.id_bebida,
            pedido.id_escuela,
            pedido.id_repartidor,
            pedido.modo_entrega,
            pedido.metodo_pago,
            pedido.cantidad
        ))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]

    def ver_por_id(self, id_pedido: int) -> Optional[Pedido]:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ver_pedido_por_id(%s)", (id_pedido,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado is None:
            return None

        return {
            "id_pedido":          resultado[0],
            "fecha_hora":         resultado[1],
            "modo_entrega":       resultado[2],
            "total":              resultado[3],
            "metodo_pago":        resultado[4],
            "cantidad":           resultado[5],
            "nombre_bebida":      resultado[6],
            "marca_bebida":       resultado[7],
            "precio_bebida":      resultado[8],
            "nombre_escuela":     resultado[9],
            "id_escuela":         resultado[10],
            "nombre_repartidor":  resultado[11],
            "id_repartidor":      resultado[12]
        }
        
    def ver_todos(self):
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM ver_pedidos()")
        resultados=cursor.fetchall()
        cursor.close()
        
        lista=[]
        for resultado in resultados:
            pedido = {
                "id_pedido":          resultado[0],
                "fecha_hora":         resultado[1],
                "modo_entrega":       resultado[2],
                "total":              resultado[3],
                "metodo_pago":        resultado[4],
                "cantidad":           resultado[5],
                "nombre_bebida":      resultado[6],
                "marca_bebida":       resultado[7],
                "precio_bebida":      resultado[8],
                "nombre_escuela":     resultado[9],
                "id_escuela":         resultado[10],
                "nombre_repartidor":  resultado[11],
                "id_repartidor":      resultado[12]
            }   
            lista.append(pedido)
        return lista