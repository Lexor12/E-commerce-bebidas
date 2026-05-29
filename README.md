# 🥤 E-commerce Bebidas

API REST para gestión de pedidos de bebidas hacia escuelas, construida con **FastAPI** y **Python** siguiendo una **arquitectura hexagonal**. La base de datos vive en **Supabase (PostgreSQL)** y toda la lógica de acceso a datos se maneja a través de sentencias SQL usando SQLAlchemy.
 
El sistema incluye un **sistema completo de autenticación y autorización** basado en **OAuth2 + JWT + Refresh Tokens**, con control de acceso por roles, y un **sistema de chat en tiempo real** con WebSockets e inteligencia artificial integrada mediante Groq.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.11+ | Lenguaje principal |
| FastAPI | Framework web / API REST |
| Uvicorn | Servidor ASGI |
| SQLAlchemy (Core) | Abstracción de queries SQL — sentencias puras sin ORM |
| psycopg2 | Driver de conexión directa a PostgreSQL |
| Pydantic | Validación y serialización de datos en endpoints |
| Supabase | Base de datos PostgreSQL en la nube |
| python-dotenv | Carga de variables de entorno desde `.env` |
| python-jose | Generación y verificación de JSON Web Tokens (JWT) |
| bcrypt | Hashing seguro de contraseñas con sal aleatoria — resistente a ataques de diccionario y rainbow tables |
| python-multipart | Soporte para form data — requerido por OAuth2PasswordRequestForm |
| groq | Cliente oficial de Groq — permite usar modelos LLM como Llama 3 de forma gratuita para el chat de soporte |
  
---

## 📋 Requisitos previos

- Python 3.11 o superior → [python.org](https://www.python.org/downloads/)
- Una cuenta en [Supabase](https://supabase.com) con un proyecto creado
- Una cuenta en [Groq](https://console.groq.com) para la IA del chat (gratuita)
- Git

---

## 🗄️ Configuración de la base de datos

### 1. Crear una Base de datos

En supabase, debes crear una nueva base de datos, asegurate de designar un nombre entendible, puede ser como "P3Bebidas", y utiliza el generador de contraseñas.

> Asegurate de guardar esa contraseña en un lugar seguro ya que se usará más tarde.

### 2. Crear las tablas
 
Las tablas se crean automáticamente al arrancar el servidor gracias a `tables.py` con `metadata.create_all(engine)`. Las tablas que se crean son:
 
| Tabla | Descripción |
|---|---|
| `Bebida` | Catálogo de bebidas disponibles |
| `Escuela` | Escuelas registradas — cada una asociada a un usuario cliente |
| `Repartidor` | Repartidores activos del sistema |
| `Pedido` | Registro inmutable de pedidos realizados |
| `Usuario` | Usuarios del sistema con rol (`cliente` o `admin`) |
| `RefreshToken` | Tokens de refresco por usuario — permiten renovar sesiones sin re-autenticarse |
| `Mensaje` | Historial de mensajes del chat — guarda mensajes del cliente y del bot |
 
> Los pedidos son **inmutables** — una vez creados no se editan ni eliminan.
 
> La tabla `Escuela` tiene un campo `id_usuario` que la asocia a un `Usuario`. Al hacer un pedido, el sistema identifica automáticamente la escuela del usuario logueado desde el token.
 
> La tabla `Mensaje` guarda todos los mensajes con `id_usuario`, `contenido`, `de` (`cliente` o `bot`) y `timestamp` — permitiendo cargar el historial de conversaciones por usuario.


### 3. Obtener la cadena de conexión

En Supabase Dashboard → **Connect** → **Direct** → **Transaction pooler**, copia la URL y reemplaza la contraseña con la contraseña antes generada en el paso anterior:

asi se deberia de ver la sentencia de conexión

```
postgresql://postgres.xxxxxx:PASSWORD@db.xxxxxx.pooler.supabase.co:5432/postgres?sslmode=require
```

debes guardarla en un archivo .env, dentro de app posteriormente, por lo que es crucial no perder la sentencia de conexión.

---

## 🤖 Configuración de IA con Groq
 
### 1. Crear cuenta y obtener API Key
 
1. Ve a [console.groq.com](https://console.groq.com)
2. Crea una cuenta gratuita — no requiere tarjeta de crédito
3. Ve a **API Keys** → **Create API Key**
4. Dale un nombre (ej. `ecommerce-bebidas`) y click **Submit**
5. **Copia la key inmediatamente** — solo se muestra una vez
### 2. Agregar la key al `.env`
 
```env
GROQ_API_KEY=gsk_tu_key_aqui
```
 
> El modelo usado es `llama-3.1-8b-instant` — gratuito, rápido y suficiente para soporte.
 
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
DATABASE_URL=postgresql://postgres.xxxxxx:PASSWORD@db.xxxxxx.pooler.supabase.co:5432/postgres?sslmode=require
SECRET_KEY=tu_clave_secreta_para_tokens
ALGORITHM="HS256"
EXPIRE_MINUTES=60
```

debes designar una clave para los tokens

> ⚠️ Nunca subas el archivo `.env` a GitHub. Ya está incluido en el `.gitignore`.

### 5. Ejecutar la app (Backend)
 
Ejecuta el proyecto, usando: 

```bash
uvicorn app.main:app --reload
```

### 6. Abrir Swagger

```
http://127.0.0.1:8000/docs
```

FastAPI genera automáticamente una interfaz visual donde puedes probar todos los endpoints.

---

### 7. Crear el primer admin

Primero dirigete a /docs y registra un usuario que será administrador, usando el endpoint de 'registrar'. Posteriormente ve al SQL Editor de Supabase y ejecuta:
 
```sql
UPDATE "Usuario" SET rol = 'admin' WHERE username = 'tu_usuario'; -- Aqui va el username de tu usuario administrador
```
 
Desde ese admin puedes promover a otros usuarios usando el endpoint `PATCH /usuario/{id}/rol`.


## 🔐 Sistema de autenticación — OAuth2 + JWT
 
El sistema implementa **OAuth2 Password Flow** con **JWT** y **Refresh Tokens**, integrado completamente dentro de la arquitectura hexagonal.
 
### Flujo completo
 
```
1. POST /registrar       → crea usuario con contraseña hasheada (bcrypt)
2. POST /login           → devuelve access_token (JWT, 60 min) + refresh_token (7 días)
3. Requests protegidos   → Authorization: Bearer <access_token>
4. POST /refresh         → cuando expira el access_token, usa el refresh_token para obtener uno nuevo
5. POST /logout          → invalida el refresh_token en BD — sesión cerrada
6. PATCH /usuario/{id}/rol → solo admins pueden cambiar roles
```
 
### Roles del sistema
 
| Rol | Acceso |
|---|---|
| `cliente` | Registrar escuela, hacer pedidos, ver catálogo, usar el chat |
| `admin` | Todo lo anterior + gestionar bebidas, repartidores, escuelas, roles y conversaciones del chat |
 
### ¿Por qué dos tokens?
 
| | Access Token | Refresh Token |
|---|---|---|
| Duración | 60 minutos | 7 días |
| Se guarda en | Cliente | Cliente + BD |
| Se manda en | Cada request | Solo en `/refresh` y `/logout` |
| Se puede invalidar | No (stateless) | Sí (logout lo desactiva en BD) |
 
El **Access Token** es un JWT firmado — el servidor lo verifica matemáticamente sin tocar la BD. El **Refresh Token** es un string aleatorio guardado en BD — permite invalidarlo en el logout sin necesidad de revocar el JWT.
 
### Seguridad de contraseñas
 
Las contraseñas se hashean con **bcrypt** antes de guardarse. bcrypt genera una **sal aleatoria** por cada hash, lo que hace imposible los ataques de diccionario y rainbow tables:
 
```
"1234" + sal_aleatoria → $2b$12$ABC...  (guardado en BD)
```
 
Al hacer login, bcrypt extrae la sal del hash guardado y la aplica al password ingresado para comparar — nunca se guarda ni se transmite la contraseña real.
 
---

## 💬 Sistema de Chat en Tiempo Real — WebSockets + IA
 
El sistema implementa un chat cliente-asistente usando **WebSockets** dentro de la arquitectura hexagonal, con respuestas automáticas por FAQ y un motor de IA integrado mediante **Groq**.


## 📡 Endpoints disponibles

### 🔓 Auth (públicos y protegidos)
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/auth/registrar` | Público | Crear cuenta de usuario |
| `POST` | `/auth/login` | Público | Iniciar sesión — devuelve tokens |
| `POST` | `/auth/refresh` | Público | Renovar access token |
| `POST` | `/auth/logout` | Público | Cerrar sesión |
| `PATCH` | `/auth/usuario/{id}/rol` | 🔒 Admin | Cambiar rol de usuario |

### 🥤 Bebidas
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/bebida` | Público | Ver todas las bebidas |
| `GET` | `/bebida/{id}` | Público | Ver bebida por ID |
| `POST` | `/bebida` | 🔒 Admin | Agregar bebida |
| `PATCH` | `/bebida/{id}` | 🔒 Admin | Editar bebida |
| `DELETE` | `/bebida/{id}` | 🔒 Admin | Desactivar bebida |
| `PATCH` | `/bebida/{id}/activar` | 🔒 Admin | Activar bebida |
 
### 🏫 Escuelas
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/escuela` | 🔒 Logueado | Ver todas las escuelas |
| `GET` | `/escuela/{id}` | 🔒 Logueado | Ver escuela por ID |
| `POST` | `/escuela` | 🔒 Logueado | Registrar escuela propia |
| `PATCH` | `/escuela/{id}` | 🔒 Admin | Editar escuela |
| `DELETE` | `/escuela/{id}` | 🔒 Admin | Desactivar escuela |
| `PATCH` | `/escuela/{id}/activar` | 🔒 Admin | Activar escuela |
 
### 🚚 Repartidores
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `GET` | `/repartidor` | 🔒 Logueado | Ver todos los repartidores |
| `GET` | `/repartidor/{id}` | 🔒 Logueado | Ver repartidor por ID |
| `POST` | `/repartidor` | 🔒 Admin | Agregar repartidor |
| `PATCH` | `/repartidor/{id}` | 🔒 Admin | Editar repartidor |
| `DELETE` | `/repartidor/{id}` | 🔒 Admin | Desactivar repartidor |
| `PATCH` | `/repartidor/{id}/activar` | 🔒 Admin | Activar repartidor |
 
### 📦 Pedidos
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/pedido` | 🔒 Logueado | Registrar pedido — la escuela se obtiene del token |
| `GET` | `/pedido/{id}` | 🔒 Logueado | Ver pedido por ID |
| `GET` | `/pedido` | 🔒 Logueado | Ver todos los pedidos |

🔒 Logueado significa que es minimo un "cliente", es decir que un Admin puede tambien usarlo

> Los pedidos son **inmutables** — una vez creados no se editan ni eliminan. Son registros históricos. El `total` y `precio_unitario` se calculan automáticamente en la BD.

---

## 🏗️ Arquitectura hexagonal


```
app/
├── domain/
│   ├── models/          → Entidades puras (Bebida, Escuela, Repartidor, Pedido,
│   │                      User, RefreshToken, Mensaje)
│   │                      Sin dependencias externas — solo Python puro
│   ├── ports/           → Contratos abstractos (ABC) que definen qué se puede hacer
│   │                      sin saber cómo se implementa
│   └── prompts/
│       └── assistant_prompt.py  → Prompt del asistente — pertenece al dominio
│                                   porque define el comportamiento del negocio,
│                                   no un detalle de infraestructura
│
├── application/
│   └── services/        → Lógica de negocio y casos de uso
│                          No sabe nada de Supabase, JWT, Groq ni FastAPI
│                          Solo trabaja con los contratos (ports)
│
├── infrastructure/
│   ├── auth/
│   │   └── jwt_service.py             → Implementación concreta de JWT (python-jose)
│   ├── faq/
│   │   ├── faq_repository.py          → Motor de FAQ por keywords con scoring
│   │   └── groq_repository.py         → Motor de IA con Llama 3 vía Groq (activo)
│   └── db/supabase/
│       ├── client.py                  → Conexión SQLAlchemy a Supabase
│       ├── tables.py                  → Definición centralizada de todas las tablas
│       └── *_supabase.py              → Implementaciones concretas de los repositorios
│
├── adapters/
│   ├── api/
│   │   ├── schemas.py                 → Modelos Pydantic (validación request/response)
│   │   └── *_router.py                → Endpoints FastAPI — solo reciben y delegan
│   └── dependencies/
│       ├── container.py               → Punto central de ensamblaje — inyección de dependencias
│       └── auth_dependency.py         → get_current_user, require_rol, verify_token_ws
├── realtime/
│   └── chat_socket.py             → WebSocket del chat — verifica JWT,
│                                    gestiona conexiones y delega al ChatService
└── main.py              → Registra todos los routers incluyendo el WebSocket
```

### Flujo de un request protegido
 
```
Request + Bearer Token
    ↓
auth_dependency.py → verifica JWT → extrae usuario y rol
    ↓
Router → valida body con Pydantic
    ↓
Service → lógica de negocio → llama al Port (ABC)
    ↓
SupabaseRepository → SQLAlchemy → PostgreSQL (Supabase)
    ↓
Response JSON ← FastAPI serializa
```
 
### Flujo de login
 
```
POST /login { username, password }
    ↓
AuthService → busca usuario en BD → verifica bcrypt
    ↓
JWTService.create_token() → genera Access Token (JWT firmado)
secrets.token_hex()       → genera Refresh Token (string aleatorio)
    ↓
RefreshToken guardado en BD
    ↓
{ access_token, refresh_token, token_type: "bearer" }
```

### Principios aplicados

- **Inversión de dependencias** — los services dependen de interfaces (ports), no de implementaciones concretas
- **Independencia de infraestructura** — cambiar Supabase por MySQL solo requiere reescribir los `*_supabase.py`
- **Independencia del mecanismo de auth** — cambiar JWT por otro sistema solo requiere reescribir `jwt_service.py`
- **Soft delete** — ninguna entidad se elimina físicamente, se desactiva con `estatus = FALSE`
- **Inyección de dependencias** — `container.py` es el único lugar donde se instancian las implementaciones concretas


---

## 📦 Dependencias

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene todas las versiones exactas usadas en el proyecto. No necesitas instalar nada más.

> Realizado por: Lexor_12