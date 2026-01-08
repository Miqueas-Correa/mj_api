from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError
from app.service.pedidos_service import crear, editar, obtener, cancelar

pedidos_bp = Blueprint("pedidos", __name__)

# Listar pedidos del usuario autenticado
@pedidos_bp.route("/pedidos/me", methods=["GET"])   #✅ Probado en postman
@jwt_required()
def get():
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener(0, get_jwt_identity(), L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Crear pedido
@pedidos_bp.route("/pedidos", methods=["POST"])  #✅ Probado en postman
@jwt_required()
def post():
    try:
        if not request.is_json: 
            return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

        data = request.json
        data["id_usuario"] = get_jwt_identity()

        crear(data)
        return jsonify({"message": "Pedido creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar pedido
# @pedidos_bp.route('/pedidos/<int:id>', methods=["PUT"])
# @jwt_required()
# def put(id):
#     try:
#         if not request.is_json: 
#             return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

#         editar(id, request.json)
#         return jsonify({"message": "Pedido modificado exitosamente"}), 200
#     except ValidationError as e:
#         return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400
#     except Exception as e:
#         return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# NUEVO - Cancelar pedido (devuelve stock)
@pedidos_bp.route('/pedidos/<int:id>/cancelar', methods=["DELETE"])
@jwt_required()
def delete_cancelar(id):
    try:
        id_usuario = get_jwt_identity()
        cancelar(id, id_usuario)
        return jsonify({"message": "Pedido cancelado exitosamente y stock devuelto"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500