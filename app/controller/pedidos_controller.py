from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.service.pedidos_service import crear, editar, eliminar, listar, obtener, crear

pedidos_bp = Blueprint("pedidos", __name__)

# Listar pedidos
@pedidos_bp.route("/pedidos", methods=["GET"])
def get():
    # listo los pedidos
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(listar(L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por id usuario
@pedidos_bp.route("/pedidos/usuario/<int:id>", methods=["GET"])
def get_id_usuario(id):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener(0, id, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por id
@pedidos_bp.route("/pedidos/<int:id>", methods=["GET"])
def get_id(id):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener(1, id, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por codigo producto
@pedidos_bp.route("/pedidos/producto/<int:codigo>", methods=["GET"])
def get_codigo_producto(codigo):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener(2, codigo, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Crear producto
@pedidos_bp.route("/pedidos", methods=["POST"])
def post():
    try:
        if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
        crear(request.json)
        return jsonify({"message": "Pedido creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar peido
@pedidos_bp.route('/pedidos/<int:id>', methods=["PUT"])
def put(id):
    try:
        if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
        editar(id, request.json)
        return jsonify({"message":"Pedido modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar producto por id
@pedidos_bp.route('/pedidos/<int:id>', methods=["DELETE"])
def delete(id):
    try:
        eliminar(id)
        return jsonify({"message":"Pedido eliminado con exito"}),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500