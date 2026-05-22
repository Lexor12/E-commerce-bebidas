# 🥤 E-commerce Bebidas

API REST para gestión de pedidos de bebidas hacia escuelas, construida con **FastAPI** y **Python** siguiendo una **arquitectura hexagonal**. La base de datos vive en **Supabase (PostgreSQL)** y toda la lógica de acceso a datos se maneja a través de funciones SQL propias.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.11+ | Lenguaje principal |
| FastAPI | Framework web / API REST |
| Uvicorn | Servidor ASGI |
| SQLAlchemy (Core) | Abstracción de queries SQL |
| psycopg2 | Driver de conexión a PostgreSQL |
| Pydantic | Validación y serialización de datos |
| Supabase | Base de datos PostgreSQL en la nube |
| python-dotenv | Manejo de variables de entorno |

---

## 📋 Requisitos previos

- Python 3.11 o superior → [python.org](https://www.python.org/downloads/)
- Una cuenta en [Supabase](https://supabase.com) con un proyecto creado
- Git

---

## 🗄️ Configuración de la base de datos

### 1. Crear las tablas

En el **SQL Editor** de tu proyecto en Supabase, ejecuta el archivo `database/bd.pgsql`. Esto creará las tablas:

```
Bebida → catálogo de bebidas
Escuela → escuelas registradas
Repartidor → repartidores activos
Pedido → registro inmutable de pedidos
```

### 2. Crear un usuario con permisos

El proyecto usa un usuario dedicado `backcommerce` con permisos únicamente sobre las funciones necesarias. El script `bd.pgsql` ya incluye al final todos los `GRANT` necesarios. Solo necesitas crear el rol en Supabase:

```sql
CREATE ROLE backcommerce WITH
  LOGIN
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  INHERIT
  NOREPLICATION
  CONNECTION LIMIT 50
  PASSWORD 'tu_password_aqui';
```

> ⚠️ El usuario `backcommerce` solo tiene permisos de ejecución sobre las funciones definidas. No tiene acceso directo a las tablas.

### 3. Obtener la cadena de conexión

En Supabase Dashboard → **Connect** → **Direct connection**, copia la URL y reemplaza el usuario por `backcommerce`:

```
postgresql://backcommerce.xxxxxx:PASSWORD@db.xxxxxx.supabase.co:5432/postgres?sslmode=require
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/E-commerce-bebidas.git
cd E-commerce-bebidas/Backend
```

### 2. Crear y activar el entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows CMD
venv\Scripts\activate

# Activar en Git Bash / Mac / Linux
source venv/Scripts/activate
```

> Sabes que está activo cuando ves `(venv)` al inicio de la terminal.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz de `Backend/` con el siguiente contenido:

```env
DATABASE_URL=postgresql://backcommerce.xxxxxx:PASSWORD@db.xxxxxx.supabase.co:5432/postgres?sslmode=require
```

> ⚠️ Nunca subas el archivo `.env` a GitHub. Ya está incluido en el `.gitignore`.

### 5. Correr el servidor

```bash
uvicorn app.main:app --reload
```

### 6. Abrir Swagger

```
http://127.0.0.1:8000/docs
```

FastAPI genera automáticamente una interfaz visual donde puedes probar todos los endpoints.

---

## 📡 Endpoints disponibles

### Bebidas
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/bebida` | Agregar bebida |
| `GET` | `/bebida` | Ver todas las bebidas |
| `GET` | `/bebida/{id}` | Ver bebida por ID |
| `PATCH` | `/bebida/{id}` | Editar bebida |
| `DELETE` | `/bebida/{id}` | Desactivar bebida |
| `PATCH` | `/bebida/{id}/activar` | Activar bebida |

### Escuelas
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/escuela` | Agregar escuela |
| `GET` | `/escuela` | Ver todas las escuelas |
| `GET` | `/escuela/{id}` | Ver escuela por ID |
| `PATCH` | `/escuela/{id}` | Editar escuela |
| `DELETE` | `/escuela/{id}` | Desactivar escuela |
| `PATCH` | `/escuela/{id}/activar` | Activar escuela |

### Repartidores
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/repartidor` | Agregar repartidor |
| `GET` | `/repartidor` | Ver todos los repartidores |
| `GET` | `/repartidor/{id}` | Ver repartidor por ID |
| `PATCH` | `/repartidor/{id}` | Editar repartidor |
| `DELETE` | `/repartidor/{id}` | Desactivar repartidor |
| `PATCH` | `/repartidor/{id}/activar` | Activar repartidor |

### Pedidos
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/pedido` | Registrar pedido |
| `GET` | `/pedido/{id}` | Ver pedido por ID |

> Los pedidos son **inmutables** — una vez creados no se editan ni eliminan. Son registros históricos. El `total` y `precio_unitario` se calculan automáticamente en la BD.

---

## 🏗️ Arquitectura hexagonal

```
app/
├── domain/
│   ├── models/          → Dataclasses puras (Escuela, Bebida, Repartidor, Pedido)
│   └── ports/           → Interfaces abstractas (ABC) — el contrato
│
├── application/
│   └── services/        → Lógica de negocio — no sabe nada de Supabase
│
├── infrastructure/
│   └── db/supabase/
│       ├── client.py    → Conexión SQLAlchemy a Supabase
│       └── *_supabase.py → Implementaciones concretas que llaman funciones SQL
│
├── adapters/
│   └── api/
│       ├── schemas.py   → Modelos Pydantic (validación request/response)
│       └── *_router.py  → Endpoints FastAPI
│
└── main.py              → Registra todos los routers
```

### Flujo de un request

```
Request JSON
    ↓ Pydantic valida
Router → Service → Port (ABC)
                       ↓
              SupabaseRepository
                       ↓ SQLAlchemy
              Función PostgreSQL
                       ↓
              Response JSON ← FastAPI serializa
```

### Principios aplicados

- **Inversión de dependencias** — los services dependen de interfaces, no de implementaciones
- **Independencia de infraestructura** — cambiar Supabase por MySQL solo requiere reescribir los `*_supabase.py`
- **Soft delete** — ninguna entidad se elimina físicamente, se desactiva con `estatus = FALSE`

---

## 🔌 Conexión a Supabase

```python
# infrastructure/db/supabase/client.py
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"], poolclass=NullPool)
```

`NullPool` — desactiva el pool de conexiones de SQLAlchemy. Recomendado para Supabase en modo serverless para evitar conexiones colgadas.

---

## 📦 Dependencias

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene todas las versiones exactas usadas en el proyecto. No necesitas instalar nada más.