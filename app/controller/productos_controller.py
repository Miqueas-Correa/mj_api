from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from service.productos_service import editar_producto, eliminar_producto_service, listar_productos_service, obtener_producto, producto_nuevo

productos_bp = Blueprint("productos", __name__)

# Listar Productos
@productos_bp.route("/productos", methods=["GET"])
def listar_productos():
    # listo los productos, en stock y sin stock
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(listar_productos_service(L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por nombre
@productos_bp.route("/productos/<string:nombre>", methods=["GET"])
def obtener_producto_por_nombre(nombre):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_producto(0, nombre, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por id
@productos_bp.route("/productos/<int:id>", methods=["GET"])
def obtener_producto_por_id(id):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_producto(1, id, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por categoria
@productos_bp.route("/productos/categoria/<string:categoria>", methods=["GET"])
def obtener_producto_por_categoria(categoria):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_producto(2, categoria, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Crear producto
@productos_bp.route("/productos", methods=["POST"])
def crear_producto():
    try:
        if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
        producto_nuevo(request.json)
        return jsonify({"message": "Producto creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar producto, este metodo permite cambiar los datos de un producto existente
@productos_bp.route('/productos/<int:id>', methods=["PUT"])
def modificar_producto(id):
    try:
        if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
        editar_producto(id, request.json, by_id=True)
        return jsonify({"message":"Producto modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar producto, este metodo permite cambiar los datos de un producto existente
@productos_bp.route('/productos/<string:nombre>', methods=["PUT"])
def modificar_producto_nombre(nombre):
    try:
        if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
        editar_producto(nombre, request.json, by_id=False)
        return jsonify({"message":"Producto modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar producto por id
@productos_bp.route('/productos/<int:id>', methods=["DELETE"])
def eliminar_producto_json(id):
    try:
        return jsonify(eliminar_producto_service(id, by_id=True)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@productos_bp.route("/productos/<string:nombre>", methods=["DELETE"])
def eliminar_producto_nombre(nombre):
    try:
        return jsonify(eliminar_producto_service(nombre, by_id=False)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500