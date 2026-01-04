from flask import Blueprint, jsonify
from app.service.productos_service import listar, obtener, categorias_list, featured

productos_bp = Blueprint("productos", __name__)

"""
Controlador de productos para la API de Flask.
Este módulo define las rutas y controladores relacionados con la gestión de productos,
incluyendo operaciones de listado, búsqueda, creación, edición y eliminación de productos,
así como la obtención de categorías y productos destacados.
Rutas:
- GET /productos: Lista todos los productos. Si el usuario es administrador, puede filtrar con el parámetro 'mostrar'.
- GET /productos/<string:nombre>: Busca un producto por nombre.
- GET /productos/<int:id>: Busca un producto por ID.
- GET /productos/categoria/<string:categoria>: Busca productos por categoría.
- GET /productos/categoria: Lista todas las categorías de productos.
- GET /productos/destacado: Lista todos los productos destacados.
- POST /productos: Crea un nuevo producto (requiere rol de administrador).
- PUT /productos/<int:id>: Modifica un producto existente por ID (requiere rol de administrador).
- DELETE /productos/<int:id>: Elimina un producto por ID (requiere rol de administrador).
Decoradores:
- @require_admin: Restringe el acceso a usuarios con rol de administrador.
- @require_user: Restringe el acceso a usuarios autenticados (no utilizado en este archivo).
Excepciones gestionadas:
- ValueError: Para errores de validación de datos o recursos no encontrados.
- ValidationError: Para errores de validación de datos con Pydantic.
- Exception: Para errores internos del servidor.
Funciones auxiliares:
- es_admin(): Verifica si el usuario actual tiene rol de administrador.
Dependencias:
- Flask (Blueprint, request, jsonify)
- Pydantic (ValidationError)
- Servicios de productos y middleware de autenticación propios de la aplicación.
"""

# Listar Productos
@productos_bp.route("/productos", methods=["GET"])
def get():
    try:
        return jsonify(listar()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por categoria
@productos_bp.route("/productos/categoria/<string:categoria>", methods=["GET"])
def get_category(categoria):
    try:
        return jsonify(obtener(2, categoria)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por nombre
@productos_bp.route("/productos/<string:nombre>", methods=["GET"])
def get_name(nombre):
    try:
        return jsonify(obtener(0, nombre)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por id
@productos_bp.route("/productos/<int:id>", methods=["GET"])
def get_id(id):
    try:
        return jsonify(obtener(1, id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar todas las categorias de los productos
@productos_bp.route("/productos/categoria", methods=["GET"])
def get_all_categories():
    try:
        return jsonify(categorias_list()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Lista todos los productos destacados
@productos_bp.route("/productos/destacado", methods=["GET"])
def get_destacados():
    try:
        return jsonify(featured()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500