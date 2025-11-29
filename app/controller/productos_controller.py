from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.service.productos_service import editar, eliminar, listar, obtener, crear, categorias_list

productos_bp = Blueprint("productos", __name__)

"""
Controlador de productos para la API de Flask.
Este módulo define las rutas y controladores relacionados con la gestión de productos,
incluyendo operaciones de listado, búsqueda, creación, edición y eliminación de productos.
Rutas:
- GET /productos: Lista todos los productos, con opción de filtrar por disponibilidad en stock.
- GET /productos/<string:nombre>: Busca un producto por su nombre.
- GET /productos/<int:id>: Busca un producto por su ID.
- GET /productos/categoria/<string:categoria>: Busca productos por categoría.
- GET /productos/categoria: Obtiene la lista de todas las categorías de productos.
- POST /productos: Crea un nuevo producto.
- PUT /productos/<int:id>: Modifica un producto existente por su ID.
- PUT /productos/<string:nombre>: Modifica un producto existente por su nombre.
- DELETE /productos/<int:id>: Elimina un producto por su ID.
- DELETE /productos/<string:nombre>: Elimina un producto por su nombre.
Excepciones manejadas:
- ValueError: Errores de validación de datos o recursos no encontrados.
- ValidationError: Errores de validación de datos de entrada (Pydantic).
- Exception: Errores internos del servidor.
Dependencias:
- Flask (Blueprint, request, jsonify)
- Pydantic (ValidationError)
- app.service.productos_service (editar, eliminar, listar, obtener, crear, categorias_list)
"""

# Listar Productos
@productos_bp.route("/productos", methods=["GET"])
def get():
    # listo los productos, en stock y sin stock
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(listar(L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por nombre
@productos_bp.route("/productos/<string:nombre>", methods=["GET"])
def get_name(nombre):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener(0, nombre, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por id
@productos_bp.route("/productos/<int:id>", methods=["GET"])
def get_id(id):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener(1, id, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por categoria
@productos_bp.route("/productos/categoria/<string:categoria>", methods=["GET"])
def get_category(categoria):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener(2, categoria, L_mostrar)), 200
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

# Crear producto
@productos_bp.route("/productos", methods=["POST"])
def post():
    try:
        if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
        crear(request.json)
        return jsonify({"message": "Producto creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar producto, este metodo permite cambiar los datos de un producto existente
@productos_bp.route('/productos/<int:id>', methods=["PUT"])
def put_id(id):
    try:
        if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
        editar(id, request.json, by_id=True)
        return jsonify({"message":"Producto modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar producto, este metodo permite cambiar los datos de un producto existente
@productos_bp.route('/productos/<string:nombre>', methods=["PUT"])
def put_name(nombre):
    try:
        if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
        editar(nombre, request.json, by_id=False)
        return jsonify({"message":"Producto modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar producto por id
@productos_bp.route('/productos/<int:id>', methods=["DELETE"])
def dalete_id(id):
    try:
        return jsonify(eliminar(id, by_id=True)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@productos_bp.route("/productos/<string:nombre>", methods=["DELETE"])
def delete_name(nombre):
    try:
        return jsonify(eliminar(nombre, by_id=False)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500