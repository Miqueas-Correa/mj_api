# mj_api

API RESTful para la gestión integral de usuarios, productos y pedidos. Diseñada con una arquitectura modular, escalable y enfocada en la facilidad de integración y mantenimiento.

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características Principales](#características-principales)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints](#endpoints)
    - [Usuarios](#usuarios)
    - [Productos](#productos)
    - [Pedidos](#pedidos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

---

## Descripción General

**mj_api** es una API desarrollada para administrar usuarios, productos y pedidos, facilitando operaciones CRUD, búsquedas avanzadas y filtrado eficiente. Su diseño modular permite una fácil extensión y mantenimiento, siendo ideal para proyectos de e-commerce o sistemas de gestión.

---

## Características Principales

- Gestión completa de usuarios, productos y pedidos.
- Filtros avanzados y búsquedas por parámetros personalizados.
- Validación robusta de datos y manejo centralizado de errores.
- Arquitectura modular y escalable.
- Documentación clara y ejemplos de uso.
- Soporte para CORS.
- Listo para pruebas y despliegue en producción.

---

## Requisitos Previos

- Python 3.8 o superior
- pip
- (Opcional) Entorno virtual recomendado

---

## Instalación

1. Clona el repositorio:
        ```bash
        git clone <URL_DEL_REPOSITORIO>
        cd mj_api
        ```

2. (Opcional) Crea y activa un entorno virtual:
        ```bash
        python -m venv venv
        # En Linux/MacOS:
        source venv/bin/activate
        # En Windows:
        .\venv\Scripts\Activate.ps1
        ```

3. Instala las dependencias:
        ```bash
        pip install -r requirements.txt
        ```

---

## Uso

1. Inicia la aplicación:
        ```bash
        flask --app app.app:create_app run
        Opcion 2:
        python -m app.app
        ```
2. Accede a la API en [http://localhost:5000/](http://localhost:5000/)

---

## Endpoints

### Usuarios

- `GET /usuarios`  
    Lista todos los usuarios. Permite filtrar por estado activo.

- `GET /usuarios?activos=true|false`  
    Filtra usuarios activos/inactivos.

- `GET /usuarios/<nombre|id>`  
    Busca usuario por nombre o ID.

- `POST /usuarios`  
    Crea un nuevo usuario.  
    **Body ejemplo:**
    ```json
    {
        "nombre": "Nombre",
        "email": "correo@ejemplo.com",
        "telefono": "2914439242",
        "contrasenia": "contraseña"
    }
    ```

- `PUT /usuarios/<id|nombre>`  
    Modifica datos del usuario.

- `DELETE /usuarios/<id|nombre>`  
    Elimina un usuario.

---

### Productos

- `GET /productos`  
    Lista todos los productos. Permite filtrar por visibilidad (`mostrar`).

- `GET /productos?mostrar=true|false`  
    Filtra productos visibles/ocultos.

- `GET /productos/<id|nombre>?mostrar=true|false`  
    Busca productos por ID o nombre.

- `GET /productos/categoria/<nombre>?mostrar=true|false`  
    Lista productos por categoría.

- `GET /productos/categoria`  
    Lista todas las categorías de productos.

- `GET /productos/destacado?mostrar=true|false`  
    Lista productos destacados.

- `POST /productos`  
    Crea un producto.  
    **Body ejemplo:**
    ```json
    {
        "categoria": "Categoria",
        "descripcion": "Descripción",
        "imagen_url": "https://...",
        "mostrar": true,
        "destacado": false,
        "nombre": "Nombre",
        "precio": 19999.99,
        "stock": 10
    }
    ```

- `PUT /productos/<id|nombre>`  
    Modifica datos del producto.

---

### Pedidos

- `GET /pedidos`  
    Lista todos los pedidos. Permite filtrar por estado (`cerrado`).

- `GET /pedidos/<id>?cerrado=true|false`  
    Busca pedido por ID.

- `GET /pedidos/usuario/<id>?cerrado=true|false`  
    Lista pedidos de un usuario.

- `GET /pedidos/producto/<id>?cerrado=true|false`  
    Lista pedidos que incluyen un producto.

- `POST /pedidos`  
    Crea un pedido.  
    **Body ejemplo:**
    ```json
    {
        "id_usuario": 1,
        "codigo_producto": 3,
        "total": 0
    }
    ```

- `PUT /pedidos/<id>`  
    Modifica un pedido.

- `DELETE /pedidos/<id>`  
    Elimina un pedido.

---

## Estructura del Proyecto

```
mj_api/
├── controller/
├── model/
├── view/
├── service/
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

---

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un _issue_ para reportar errores o sugerir mejoras, o envía un _pull request_ para contribuir directamente.

---

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

---
