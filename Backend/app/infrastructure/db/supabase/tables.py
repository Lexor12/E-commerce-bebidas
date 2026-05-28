# tables.py
from app.infrastructure.db.supabase.client import engine
from sqlalchemy import Table, Column, Integer, Numeric, Boolean, String, MetaData, DateTime, ForeignKey

metadata = MetaData()

tabla_bebida = Table(
    "Bebida", metadata,
    Column("id_bebida", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String),
    Column("marca", String),
    Column("litros", Numeric),
    Column("cantidad", Integer),
    Column("precio", Numeric),
    Column("ingredientes", String),
    Column("advertencias", String),
    Column("estatus", Boolean, default=True)
)

tabla_escuela = Table(
    "Escuela", metadata,
    Column("id_escuela", Integer, primary_key=True, autoincrement=True),
    Column("id_usuario", Integer),
    Column("nombre", String),
    Column("ubicacion", String),
    Column("nivel_academico", String),
    Column("telefono", String),
    Column("estatus", Boolean, default=True)
)

tabla_repartidor = Table(
    "Repartidor", metadata,
    Column("id_repartidor", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String),
    Column("fecha_ingreso", DateTime),
    Column("calificacion", Numeric),
    Column("telefono", String),
    Column("estatus", Boolean, default=True)
)

tabla_usuario = Table(
    "Usuario", metadata,
    Column("id_usuario", Integer, primary_key=True, autoincrement=True),
    Column("username", String),
    Column("password", String),
    Column("rol", String)
)

tabla_refresh_token = Table(
    "RefreshToken", metadata,
    Column("id_token", Integer, primary_key=True, autoincrement=True),
    Column("token", String),
    Column("id_usuario", Integer),
    Column("expira", DateTime),
    Column("activo", Boolean, default=True)
)

tabla_pedido = Table(
    "Pedido", metadata,
    Column("id_pedido", Integer, primary_key=True, autoincrement=True),
    Column("id_bebida", Integer, ForeignKey("Bebida.id_bebida")),
    Column("id_escuela", Integer, ForeignKey("Escuela.id_escuela")),
    Column("id_repartidor", Integer, ForeignKey("Repartidor.id_repartidor")),
    Column("fecha_hora", DateTime),
    Column("modo_entrega", String),
    Column("total", Numeric),
    Column("precio_unitario", Numeric),
    Column("metodo_pago", String),
    Column("cantidad", Integer)
)

metadata.create_all(engine)