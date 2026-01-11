from flask import Blueprint, jsonify
from app.service.productos_service import listar, obtener, categorias_list, featured
"""
Controlador de productos para la API.
Rutas:
- GET /productos: Lista todos los productos.
- GET /productos/categoria/<string:categoria>: Busca productos por categoría.
- GET /productos/<string:nombre>: Busca productos por nombre.
- GET /productos/<int:id>: Busca producto por ID.
- GET /productos/categoria: Lista todas las categorías de productos.
- GET /productos/destacado: Lista todos los productos destacados.
Cada endpoint maneja errores de valor y errores internos del servidor, devolviendo mensajes apropiados en formato JSON.
"""

productos_bp = Blueprint("productos", __name__)

# Listar Productos
@productos_bp.route("/productos", methods=["GET"]) #✅ Probado en postman
def get():
    try:
        return jsonify(listar()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por categoria
@productos_bp.route("/productos/categoria/<string:categoria>", methods=["GET"]) # ✅ Probado en postman
def get_category(categoria):
    try:
        return jsonify(obtener(2, categoria)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por nombre
@productos_bp.route("/productos/<string:nombre>", methods=["GET"])  #✅ Probado en postman
def get_name(nombre):
    try:
        return jsonify(obtener(0, nombre)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por id
@productos_bp.route("/productos/<int:id>", methods=["GET"]) #✅ Probado en postman
def get_id(id):
    try:
        return jsonify(obtener(1, id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar todas las categorias de los productos
@productos_bp.route("/productos/categoria", methods=["GET"])    #✅ Probado en postman
def get_all_categories():
    try:
        return jsonify(categorias_list()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Lista todos los productos destacados
@productos_bp.route("/productos/destacado", methods=["GET"])    #✅ Probado en postman
def get_destacados():
    try:
        return jsonify(featured()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500