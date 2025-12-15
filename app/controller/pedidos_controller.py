from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.controller.auth_middleware import require_admin, require_user
from app.service.pedidos_service import crear, editar, eliminar, listar, obtener, crear

pedidos_bp = Blueprint("pedidos", __name__)

"""
Controlador de pedidos para la API.
Este módulo define las rutas y controladores relacionados con la gestión de pedidos en la aplicación.
Incluye funcionalidades para listar, buscar, crear, modificar y eliminar pedidos, con control de acceso
según el rol del usuario (admin o usuario regular).
Blueprint:
    pedidos_bp: Blueprint de Flask para agrupar las rutas de pedidos.
Funciones:
    es_admin():
        Verifica si el usuario autenticado tiene rol de administrador.
    get():
        Lista los pedidos. Los administradores ven todos los pedidos, los usuarios solo los suyos.
        Parámetros opcionales por query: 'cerrado' (str).
    get_id_usuario(id):
        Busca pedidos por ID de usuario. Solo accesible por administradores.
        Parámetros opcionales por query: 'cerrado' (str).
    get_id(id):
        Busca un pedido por su ID. Accesible por usuarios autenticados.
        Parámetros opcionales por query: 'cerrado' (str).
    get_codigo_producto(codigo):
        Busca pedidos por código de producto. Solo accesible por administradores.
        Parámetros opcionales por query: 'cerrado' (str).
    post():
        Crea un nuevo pedido. Los usuarios solo pueden crear pedidos para sí mismos.
        Requiere datos en formato JSON.
    put(id):
        Modifica un pedido existente por su ID. Solo accesible por administradores.
        Requiere datos en formato JSON.
    delete(id):
        Elimina un pedido por su ID. Solo accesible por administradores.
Excepciones:
    - ValidationError: Error de validación de datos de entrada.
    - ValueError: Error de valor en los parámetros o datos.
    - Exception: Otros errores internos del servidor.
Decoradores:
    - @require_user: Requiere autenticación de usuario.
    - @require_admin: Requiere autenticación de administrador.
"""

def es_admin():
    return request.user_rol == "admin"

# Listar pedidos, token requerido
@require_user
@pedidos_bp.route("/pedidos", methods=["GET"])
def get():
    # listo los pedidos
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)

        if es_admin():
            # admin ve todos
            return jsonify(listar(L_cerrado)), 200
        else:
            # usuario solo sus pedidos
            return jsonify(obtener(0, request.user_id, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por id usuario
@require_admin
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
@require_user
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
@require_admin
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
@require_user
@pedidos_bp.route("/pedidos", methods=["POST"])
def post():
    try:
        if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400

        data = request.json

        if not es_admin(): data["id_usuario"] = request.user_id

        crear(data)
        return jsonify({"message": "Pedido creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar pedido
@require_admin
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
@require_admin
@pedidos_bp.route('/pedidos/<int:id>', methods=["DELETE"])
def delete(id):
    try:
        eliminar(id)
        return jsonify({"message":"Pedido eliminado con exito"}),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500