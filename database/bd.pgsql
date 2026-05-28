-- ============================================================
--  TABLAS
-- ============================================================

DROP TABLE IF EXISTS "Pedido";
DROP TABLE IF EXISTS "Bebida";
DROP TABLE IF EXISTS "Escuela";
DROP TABLE IF EXISTS "Repartidor";

CREATE TABLE "Bebida" (
  "id_bebida" SERIAL,
  "nombre" TEXT,
  "marca" TEXT,
  "litros" DECIMAL,
  "cantidad" INT,
  "precio" DECIMAL,
  "ingredientes" TEXT,
  "advertencias" TEXT,
  "estatus" BOOLEAN,
  PRIMARY KEY ("id_bebida")
);

CREATE TABLE "Escuela" (
  "id_escuela" SERIAL,
  "id_usuario" INT,
  "nombre" TEXT,
  "ubicacion" TEXT,
  "nivel_academico" TEXT,
  "telefono" TEXT,
  "estatus" BOOLEAN,
  PRIMARY KEY ("id_escuela")
);

CREATE TABLE "Repartidor" (
  "id_repartidor" SERIAL,
  "nombre" TEXT,
  "fecha_ingreso" TIMESTAMP,
  "calificacion" DECIMAL,
  "telefono" TEXT,
  "estatus" BOOLEAN,
  PRIMARY KEY ("id_repartidor")
);

CREATE TABLE "Pedido" (
  "id_pedido" SERIAL,
  "id_bebida" INT,
  "id_escuela" INT,
  "id_repartidor" INT,
  "fecha_hora" TIMESTAMP,
  "modo_entrega" TEXT,
  "total" DECIMAL,
  "precio_unitario" DECIMAL,
  "metodo_pago" TEXT,
  "cantidad" INT,
  PRIMARY KEY ("id_pedido"),
  CONSTRAINT "FK_Pedido_id_escuela"
    FOREIGN KEY ("id_escuela")
    REFERENCES "Escuela"("id_escuela"),
  CONSTRAINT "FK_Pedido_id_bebida"
    FOREIGN KEY ("id_bebida")
    REFERENCES "Bebida"("id_bebida"),
  CONSTRAINT "FK_Pedido_id_repartidor"
    FOREIGN KEY ("id_repartidor")
    REFERENCES "Repartidor"("id_repartidor")
);
CREATE TABLE "Usuario" (
    id_usuario SERIAL PRIMARY KEY,
    username   VARCHAR(48) UNIQUE NOT NULL,
    password   VARCHAR(256) NOT NULL,
    rol        VARCHAR(20) DEFAULT 'cliente'
);
CREATE TABLE "RefreshToken" (
    id_token SERIAL PRIMARY KEY,
    token VARCHAR(256) UNIQUE NOT NULL,
    id_usuario INTEGER NOT NULL,
    expira TIMESTAMP NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

CREATE ROLE backcommerce WITH 
  LOGIN 
  NOSUPERUSER 
  NOCREATEDB 
  NOCREATEROLE 
  INHERIT 
  NOREPLICATION
  CONNECTION LIMIT 50 
  PASSWORD ''; -- Aqui va la contraseña del usuario

-- NOTA
-- Asegurarse de que todas las tablas tienen RLS dentro de supabase y asegurarte de dar todos los permisos a tu usuario