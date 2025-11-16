# mj_api

---

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints Principales](#endpoints-principales)
    - [Usuarios](#usuarios)
    - [Productos](#productos)
    - [Pedidos](#pedidos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Características

- Gestión de usuarios, productos y pedidos.
- Filtros avanzados y búsquedas por distintos parámetros.
- Validación de datos y manejo de errores.
- Arquitectura modular y escalable.
- Documentación clara de endpoints y ejemplos de uso.

---

## Instalación

1. Clona el repositorio:
     ```bash
     git clone <URL_DEL_REPOSITORIO>
     cd mj_api
     ```

2. Crea un entorno virtual (opcional pero recomendado):
     ```bash
     python -m venv venv
     source venv/bin/activate  # En Windows: venv\Scripts\activate
     ```

3. Instala las dependencias:
     ```bash
     pip install -r requirements.txt
     ```

---

## Uso

1. Inicia la aplicación:
     ```bash
     flask run
     ```
2. Accede a la API en `http://localhost:5000/`.

---

## Endpoints Principales

### Usuarios

- **GET /usuarios**  
    Lista todos los usuarios. Permite filtrar por estado activo.

- **GET /usuarios?activos=true|false**  
    Filtra usuarios activos/inactivos.

- **GET /usuarios/<nombre|id>**  
    Busca usuario por nombre o ID.

- **POST /usuarios**  
    Crea un nuevo usuario.  
    _Body requerido:_
    ```json
    {
        "nombre": "Nombre",
        "email": "correo@ejemplo.com",
        "telefono": "2914439242",
        "contrasenia": "contraseña"
    }
    ```

- **PUT /usuarios/<id|nombre>**  
    Modifica datos del usuario.

- **DELETE /usuarios/<id|nombre>**  
    Elimina un usuario.

---

### Productos

- **GET /productos**  
    Lista todos los productos. Permite filtrar por visibilidad (`mostrar`).

- **GET /productos?mostrar=true|false**  
    Filtra productos visibles/ocultos.

- **GET /productos/<id|nombre>?mostrar=true|false**  
    Busca productos por ID o nombre.

- **GET /productos/categoria/<nombre>?mostrar=true|false**  
    Lista productos por categoría.

- **POST /productos**  
    Crea un producto.  
    _Body requerido:_
    ```json
    {
        "categoria": "Categoria",
        "descripcion": "Descripción",
        "imagen_url": "https://...",
        "mostrar": true,
        "nombre": "Nombre",
        "precio": 19999.99,
        "stock": 10
    }
    ```

- **PUT /productos/<id|nombre>**  
    Modifica datos del producto.

---

### Pedidos

- **GET /pedidos**  
    Lista todos los pedidos. Permite filtrar por estado (`cerrado`).

- **GET /pedidos/<id>?cerrado=true|false**  
    Busca pedido por ID.

- **GET /pedidos/usuario/<id>?cerrado=true|false**  
    Lista pedidos de un usuario.

- **GET /pedidos/producto/<id>?cerrado=true|false**  
    Lista pedidos que incluyen un producto.

- **POST /pedidos**  
    Crea un pedido.  
    _Body requerido:_
    ```json
    {
        "id_usuario": 1,
        "codigo_producto": 3,
        "total": 0
    }
    ```

- **PUT /pedidos/<id>**  
    Modifica un pedido.

- **DELETE /pedidos/<id>**  
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

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un _issue_ o envía un _pull request_ para sugerencias o mejoras.

---

## Licencia

Este proyecto está bajo la licencia MIT.

---
