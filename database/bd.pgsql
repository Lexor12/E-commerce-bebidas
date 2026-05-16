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

-- Funcion para crear escuelas

-- Funcion para crear escuelas
CREATE OR REPLACE FUNCTION agregar_escuela(p_nombre TEXT,p_ubicacion TEXT,p_nivel_academico TEXT,p_telefono TEXT
) RETURNS INT SECURITY DEFINER SET search_path = public AS $$
DECLARE v_id INT;
BEGIN
    INSERT INTO "Escuela"(nombre, ubicacion, nivel_academico, telefono, estatus)
    VALUES (p_nombre, p_ubicacion, p_nivel_academico, p_telefono, TRUE)
    RETURNING id_escuela INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;


-- Ver escuela por ID
CREATE OR REPLACE FUNCTION ver_escuela_por_id(p_id_escuela INT)
RETURNS TABLE(id_escuela INT,nombre TEXT,ubicacion TEXT,nivel_academico TEXT,telefono TEXT,estatus BOOLEAN
) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    RETURN QUERY
    SELECT e."id_escuela", e."nombre", e."ubicacion", e."nivel_academico", e."telefono", e."estatus"
    FROM "Escuela" AS e
    WHERE e."id_escuela" = p_id_escuela;
END;
$$ LANGUAGE plpgsql;


-- Editar escuela por ID
CREATE OR REPLACE FUNCTION editar_escuela_por_id(p_id_escuela INT,p_nombre TEXT DEFAULT NULL,p_ubicacion TEXT DEFAULT NULL,p_nivel_academico TEXT DEFAULT NULL,p_telefono TEXT DEFAULT NULL
) RETURNS TEXT SECURITY DEFINER SET search_path = public AS $$
BEGIN
    UPDATE "Escuela"
    SET
        nombre = COALESCE(p_nombre,          nombre),
        ubicacion = COALESCE(p_ubicacion,       ubicacion),
        nivel_academico = COALESCE(p_nivel_academico, nivel_academico),
        telefono = COALESCE(p_telefono,        telefono)
    WHERE id_escuela = p_id_escuela AND estatus = TRUE;

    IF NOT FOUND THEN RETURN 'Escuela no encontrada o inactiva.'; END IF;
    RETURN 'Escuela actualizada correctamente.';
END;
$$ LANGUAGE plpgsql;


-- Desactivar escuela (soft delete)
CREATE OR REPLACE FUNCTION desactivar_escuela_por_id(p_id_escuela INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Escuela" WHERE id_escuela = p_id_escuela AND estatus = TRUE) THEN
        status  := 0;
        mensaje := 'Escuela no encontrada o ya inactiva.';
        RETURN NEXT;
        RETURN;
    END IF;

    UPDATE "Escuela" SET estatus = FALSE WHERE id_escuela = p_id_escuela;
    status  := 1;
    mensaje := 'Escuela desactivada correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Activar escuela 
CREATE OR REPLACE FUNCTION activar_escuela_por_id(p_id_escuela INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Escuela" WHERE id_escuela = p_id_escuela AND estatus = FALSE) THEN
        status  := 0;
        mensaje := 'Escuela no encontrada o ya activa.';
        RETURN NEXT;
        RETURN;
    END IF;
    UPDATE "Escuela" SET estatus = TRUE WHERE id_escuela = p_id_escuela;
    status  := 1;
    mensaje := 'Escuela activada correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
--  REPARTIDOR
-- ============================================================

-- Agregar repartidor
CREATE OR REPLACE FUNCTION agregar_repartidor(p_nombre TEXT,p_fecha_ingreso TIMESTAMP,p_calificacion DECIMAL,p_telefono TEXT
) RETURNS INT SECURITY DEFINER SET search_path = public AS $$
DECLARE v_id INT;
BEGIN
    INSERT INTO "Repartidor"(nombre, fecha_ingreso, calificacion, telefono, estatus)
    VALUES (p_nombre, p_fecha_ingreso, p_calificacion, p_telefono, TRUE)
    RETURNING id_repartidor INTO v_id;--Esto basicamente guarda la ID que se acaba de crear en la variable
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Ver repartidor por ID
CREATE OR REPLACE FUNCTION ver_repartidor_por_id(p_id_repartidor INT)
RETURNS TABLE(id_repartidor INT,nombre TEXT,fecha_ingreso TIMESTAMP,calificacion DECIMAL,telefono TEXT,estatus BOOLEAN) 
SECURITY DEFINER SET search_path = public AS $$
BEGIN
    RETURN QUERY
    SELECT r."id_repartidor", r."nombre", r."fecha_ingreso", r."calificacion", r."telefono", r."estatus"
    FROM "Repartidor" AS r
    WHERE r."id_repartidor" = p_id_repartidor;
END;
$$ LANGUAGE plpgsql;


-- Editar repartidor por ID
CREATE OR REPLACE FUNCTION editar_repartidor_por_id(p_id_repartidor INT,p_nombre TEXT DEFAULT NULL,p_calificacion DECIMAL DEFAULT NULL,p_telefono TEXT DEFAULT NULL) 
RETURNS TEXT SECURITY DEFINER SET search_path = public AS $$
BEGIN
    UPDATE "Repartidor"
    SET
        nombre = COALESCE(p_nombre,nombre),
        calificacion = COALESCE(p_calificacion, calificacion),
        telefono = COALESCE(p_telefono,telefono)
    WHERE id_repartidor = p_id_repartidor AND estatus = TRUE;

    IF NOT FOUND THEN RETURN 'Repartidor no encontrado o inactivo.'; END IF;
    RETURN 'Repartidor actualizado correctamente.';
END;
$$ LANGUAGE plpgsql;


-- Desactivar repartidor (soft delete)
CREATE OR REPLACE FUNCTION desactivar_repartidor_por_id(p_id_repartidor INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Repartidor" WHERE id_repartidor = p_id_repartidor AND estatus = TRUE) THEN
        status  := 0;
        mensaje := 'Repartidor no encontrado o ya inactivo.';
        RETURN NEXT;
        RETURN;
    END IF;

    UPDATE "Repartidor" SET estatus = FALSE WHERE id_repartidor = p_id_repartidor;
    status  := 1;
    mensaje := 'Repartidor desactivado correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Activar repartidor 
CREATE OR REPLACE FUNCTION activar_repartidor_por_id(p_id_repartidor INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Repartidor" WHERE id_repartidor = p_id_repartidor AND estatus = FALSE) THEN
        status  := 0;
        mensaje := 'Repartidor no encontrado o ya activo.';
        RETURN NEXT;
        RETURN;
    END IF;

    UPDATE "Repartidor" SET estatus = TRUE WHERE id_repartidor = p_id_repartidor;
    status  := 1;
    mensaje := 'Repartidor activado correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
--  BEBIDA
-- ============================================================

-- Agregar bebida
CREATE OR REPLACE FUNCTION agregar_bebida(p_nombre TEXT,p_marca TEXT,p_litros DECIMAL,p_cantidad INT,p_precio DECIMAL,p_ingredientes TEXT,p_advertencias TEXT)
RETURNS INT SECURITY DEFINER SET search_path = public AS $$
DECLARE v_id INT;
BEGIN
    INSERT INTO "Bebida"(nombre, marca, litros, cantidad, precio, ingredientes, advertencias, estatus)
    VALUES (p_nombre, p_marca, p_litros, p_cantidad, p_precio, p_ingredientes, p_advertencias, TRUE)
    RETURNING id_bebida INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Ver bebida por ID
CREATE OR REPLACE FUNCTION ver_bebida_por_id(p_id_bebida INT)
RETURNS TABLE(id_bebida INT,nombre TEXT,marca TEXT,litros DECIMAL,cantidad INT,precio DECIMAL,ingredientes TEXT,advertencias TEXT,estatus BOOLEAN)
SECURITY DEFINER SET search_path = public AS $$
BEGIN
    RETURN QUERY
    SELECT b."id_bebida", b."nombre", b."marca", b."litros", b."cantidad", b."precio", b."ingredientes", b."advertencias", b."estatus"
    FROM "Bebida" AS b
    WHERE b."id_bebida" = p_id_bebida;
END;
$$ LANGUAGE plpgsql;

-- Editar bebida por ID
CREATE OR REPLACE FUNCTION editar_bebida_por_id(p_id_bebida INT,p_nombre TEXT DEFAULT NULL,p_marca TEXT DEFAULT NULL,p_litros DECIMAL DEFAULT NULL,p_cantidad INT DEFAULT NULL,p_precio DECIMAL DEFAULT NULL,p_ingredientes TEXT DEFAULT NULL,p_advertencias TEXT DEFAULT NULL)
RETURNS TEXT SECURITY DEFINER SET search_path = public AS $$
BEGIN
    UPDATE "Bebida"
    SET
        nombre = COALESCE(p_nombre,nombre),
        marca = COALESCE(p_marca,marca),
        litros = COALESCE(p_litros,litros),
        cantidad = COALESCE(p_cantidad,cantidad),
        precio = COALESCE(p_precio,precio),
        ingredientes = COALESCE(p_ingredientes, ingredientes),
        advertencias = COALESCE(p_advertencias, advertencias)
    WHERE id_bebida = p_id_bebida AND estatus = TRUE;

    IF NOT FOUND THEN RETURN 'Bebida no encontrada o inactiva.'; END IF;
    RETURN 'Bebida actualizada correctamente.';
END;
$$ LANGUAGE plpgsql;

-- Desactivar bebida (soft delete)
CREATE OR REPLACE FUNCTION desactivar_bebida_por_id(p_id_bebida INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Bebida" WHERE id_bebida = p_id_bebida AND estatus = TRUE) THEN
        status  := 0;
        mensaje := 'Bebida no encontrada o ya inactiva.';
        RETURN NEXT;
        RETURN;
    END IF;

    UPDATE "Bebida" SET estatus = FALSE WHERE id_bebida = p_id_bebida;
    status  := 1;
    mensaje := 'Bebida desactivada correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Activar bebida
CREATE OR REPLACE FUNCTION activar_bebida_por_id(p_id_bebida INT)
RETURNS TABLE(status INT, mensaje TEXT) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Bebida" WHERE id_bebida = p_id_bebida AND estatus = FALSE) THEN
        status  := 0;
        mensaje := 'Bebida no encontrada o ya activa.';
        RETURN NEXT;
        RETURN;
    END IF;

    UPDATE "Bebida" SET estatus = TRUE WHERE id_bebida = p_id_bebida;
    status  := 1;
    mensaje := 'Bebida activada correctamente.';
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
-- PEDIDO
-- ============================================================

-- Agregar pedido
CREATE OR REPLACE FUNCTION agregar_pedido(p_id_bebida INT,p_id_escuela INT,p_id_repartidor INT,p_modo_entrega TEXT,p_total DECIMAL,p_metodo_pago TEXT,p_cantidad INT)
RETURNS TEXT SECURITY DEFINER SET search_path = public AS $$
DECLARE v_id INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM "Bebida" WHERE id_bebida = p_id_bebida AND estatus = TRUE) THEN
        RETURN 'Error: La bebida no existe o está inactiva.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM "Escuela" WHERE id_escuela = p_id_escuela AND estatus = TRUE) THEN
        RETURN 'Error: La escuela no existe o está inactiva.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM "Repartidor" WHERE id_repartidor = p_id_repartidor AND estatus = TRUE) THEN
        RETURN 'Error: El repartidor no existe o está inactivo.';
    END IF;

    INSERT INTO "Pedido"(id_bebida, id_escuela, id_repartidor, fecha_hora, modo_entrega, total, metodo_pago, cantidad)
    VALUES (p_id_bebida, p_id_escuela, p_id_repartidor, NOW(), p_modo_entrega, p_total, p_metodo_pago, p_cantidad)
    RETURNING id_pedido INTO v_id;

    RETURN 'Pedido #' || v_id || ' registrado correctamente.';--Aqui si combiene poner text, ya que hay varios errores
END;
$$ LANGUAGE plpgsql;

-- Ver pedido por ID (con datos relacionados aplanados)
CREATE OR REPLACE FUNCTION ver_pedido_por_id(p_id_pedido INT)
RETURNS TABLE(
    id_pedido INT,
    fecha_hora TIMESTAMP,
    modo_entrega TEXT,
    total DECIMAL,
    metodo_pago TEXT,
    cantidad INT,
    nombre_bebida TEXT,
    marca_bebida TEXT,
    precio_bebida DECIMAL,
    nombre_escuela TEXT,
    id_escuela INT,
    nombre_repartidor TEXT,
    id_repartidor INT
) SECURITY DEFINER SET search_path = public AS $$
BEGIN
    RETURN QUERY
    SELECT
        pe."id_pedido", pe."fecha_hora", pe."modo_entrega", pe."total", pe."metodo_pago", pe."cantidad",b."nombre",  b."marca",  b."precio",e."nombre",e."id_escuela",r."nombre",r."id_repartidor"
    FROM  "Pedido" AS pe
    JOIN  "Bebida" AS b ON b."id_bebida"= pe."id_bebida"
    JOIN  "Escuela" AS e ON e."id_escuela"    = pe."id_escuela"
    JOIN  "Repartidor" AS r ON r."id_repartidor" = pe."id_repartidor"
    WHERE pe."id_pedido" = p_id_pedido;
END;
$$ LANGUAGE plpgsql;


-- ============================================================
--  GRANTs para el usuario backcommerce
-- ============================================================

GRANT CONNECT ON DATABASE postgres TO backcommerce;
GRANT USAGE ON SCHEMA public TO backcommerce;

-- CATEGORÍA: ESCUELAS
GRANT EXECUTE ON FUNCTION agregar_escuela(TEXT, TEXT, TEXT, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION ver_escuela_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION editar_escuela_por_id(INT, TEXT, TEXT, TEXT, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION desactivar_escuela_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION activar_escuela_por_id(INT) TO backcommerce;

-- CATEGORÍA: REPARTIDORES
GRANT EXECUTE ON FUNCTION agregar_repartidor(TEXT, TIMESTAMP, DECIMAL, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION ver_repartidor_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION editar_repartidor_por_id(INT, TEXT, DECIMAL, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION desactivar_repartidor_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION activar_repartidor_por_id(INT) TO backcommerce;

-- CATEGORÍA: BEBIDAS
GRANT EXECUTE ON FUNCTION agregar_bebida(TEXT, TEXT, DECIMAL, INT, DECIMAL, TEXT, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION ver_bebida_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION editar_bebida_por_id(INT, TEXT, TEXT, DECIMAL, INT, DECIMAL, TEXT, TEXT) TO backcommerce;
GRANT EXECUTE ON FUNCTION desactivar_bebida_por_id(INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION activar_bebida_por_id(INT) TO backcommerce;

-- CATEGORÍA: PEDIDOS
GRANT EXECUTE ON FUNCTION agregar_pedido(INT, INT, INT, TEXT, DECIMAL, TEXT, INT) TO backcommerce;
GRANT EXECUTE ON FUNCTION ver_pedido_por_id(INT) TO backcommerce;

CREATE ROLE backcommerce WITH 
  LOGIN 
  NOSUPERUSER 
  NOCREATEDB 
  NOCREATEROLE 
  INHERIT 
  NOREPLICATION
  CONNECTION LIMIT 50 
  PASSWORD '';