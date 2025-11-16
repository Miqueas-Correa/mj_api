from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.service.pedidos_service import crear, editar, eliminar, listar, obtener, crear

pedidos_bp = Blueprint("pedidos", __name__)

"""
Controlador de pedidos para la API de Flask.
Este módulo define las rutas relacionadas con la gestión de pedidos, incluyendo operaciones para listar, buscar, crear, modificar y eliminar pedidos. Utiliza servicios definidos en `app.service.pedidos_service` para realizar la lógica de negocio.
Rutas:
- GET /pedidos: Lista todos los pedidos, opcionalmente filtrados por el parámetro 'cerrado'.
- GET /pedidos/usuario/<int:id>: Obtiene los pedidos asociados a un usuario específico, con opción de filtrar por 'cerrado'.
- GET /pedidos/<int:id>: Obtiene un pedido por su ID, con opción de filtrar por 'cerrado'.
- GET /pedidos/producto/<int:codigo>: Obtiene los pedidos asociados a un producto específico, con opción de filtrar por 'cerrado'.
- POST /pedidos: Crea un nuevo pedido. Requiere un cuerpo JSON válido.
- PUT /pedidos/<int:id>: Modifica un pedido existente identificado por su ID. Requiere un cuerpo JSON válido.
- DELETE /pedidos/<int:id>: Elimina un pedido por su ID.
Manejo de errores:
- Devuelve mensajes de error claros para errores de validación, errores de valor y errores internos del servidor.
- Utiliza códigos de estado HTTP apropiados para cada situación.
Dependencias:
- Flask: Para la definición de rutas y manejo de solicitudes/respuestas.
- Pydantic: Para la validación de datos de entrada.
- app.service.pedidos_service: Contiene la lógica de negocio para las operaciones de pedidos.
"""

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