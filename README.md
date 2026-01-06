# MJ API – Backend

Backend de la tienda virtual MJ, desarrollado como una API REST, encargado de gestionar la lógica de negocio, autenticación, seguridad y persistencia de datos de usuarios, productos y pedidos.

Este proyecto forma parte de un sistema completo Frontend + Backend, diseñado bajo buenas prácticas de arquitectura de software y pensado para evolucionar en el tiempo.

## Tecnologías Utilizadas

Python

Flask

Flask-JWT-Extended

Flask-SQLAlchemy

Pydantic

MySQL

Werkzeug (password hashing)

dotenv

Postman (testing de endpoints)

## Arquitectura del Proyecto

La API está organizada siguiendo una arquitectura modular, separando responsabilidades:

Controladores (routes)

Servicios (lógica de negocio)

Modelos (base de datos)

Validaciones

Seguridad (JWT)

Esto permite:

Escalabilidad

Mantenimiento sencillo

Código limpio y testeable

## Estructura del Proyecto
- mj_api/
- │
- ├── app/
- │   ├── app.py
- │   ├── config.py
- │   ├── extensions.py
- │
- │   ├── controllers/
- │   │   ├── auth_controller.py
- │   │   ├── usuarios_controller.py
- │   │   ├── productos_controller.py
- │   │   └── pedidos_controller.py
- │
- │   ├── models/
- │   │   ├── usuario.py
- │   │   ├── producto.py
- │   │   ├── pedido.py
- │   │   └── token_blacklist.py
- │
- │   ├── schemas/
- │   │   ├── usuario_schema.py
- │   │   ├── producto_schema.py
- │   │   └── pedido_schema.py
- │
- │   ├── services/
- │   │   ├── usuarios_service.py
- │   │   ├── productos_service.py
- │   │   └── pedidos_service.py
- │
- │   └── utils/
- │       └── security.py
- │
- ├── migrations/
- ├── tests/
- │
- ├── .env.example
- ├── requirements.txt
- ├── run.py
- └── README.md

## Autenticación y Seguridad

La API utiliza JWT (JSON Web Tokens) para la autenticación.

Características:

Login con token de acceso

Refresh token

Logout con blacklist de tokens

Protección de rutas

Roles de usuario (cliente / administrador)

Esto garantiza:

Seguridad

Control de acceso

Buenas prácticas reales de backend

## Base de Datos

Base de datos relacional MySQL, modelada con SQLAlchemy.

- Entidades principales:

* Usuarios

* Productos

* Pedidos

* Tokens revocados

## Endpoints Principales
- Autenticación

POST /auth/login

POST /auth/logout

POST /auth/refresh

- Usuarios

GET /usuarios

POST /usuarios

PUT /usuarios/{id}

DELETE /usuarios/{id}

- Productos

GET /productos

POST /productos

PUT /productos/{id}

DELETE /productos/{id}

- Pedidos

GET /pedidos

POST /pedidos

GET /pedidos/{id}

📌 Todos los endpoints protegidos requieren token JWT.

## Instalación y Ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/Miqueas-Correa/mj_api.git
cd mj_api

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Variables de entorno

Crear un archivo .env basado en .env.example
- Base de datos
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=mj_db

- Entorno
FLASK_ENV=production
DEBUG=False

- Seguridad
JWT_SECRET_KEY=your_jwt_secret_key

- CORS
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

- Backend
BACKEND_URL=http://localhost:5000

## Ejecutar la API
python -m app.app


Servidor disponible en:

http://localhost:5000

## Testing

Tests unitarios incluidos

Endpoints testeados con Postman

Colección Postman incluida como parte de la documentación

## Integración con el Frontend

Este backend es consumido por el frontend MJ Frontend (React + Vite).

La separación entre:

Cliente público

Cliente administrador

permite un sistema seguro y escalable.

## Despliegue

El backend está preparado para ser desplegado en plataformas como:

Render

Railway

Heroku

Incluye:

Variables de entorno

Configuración productiva

Manejo de migraciones

## Proyecto en Evolución

El backend de MJ está diseñado para seguir creciendo.
Entre las mejoras planificadas:

Historial de pedidos

Estados de pedido

Roles avanzados

Reportes y métricas

Paginación y filtros

Optimización de consultas

## Autor

Miqueas Correa
Backend / Full Stack Developer
📍 Bahía Blanca, Buenos Aires, Argentina

GitHub: Miqueas-Correa

LinkedIn: miqueas-correa

## 📌 Notas Finales

Este backend representa una API REST realista, segura y escalable, alineada con prácticas profesionales y académicas, integrándose con un frontend moderno para conformar la tienda virtual MJ.