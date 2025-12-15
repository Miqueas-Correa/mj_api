from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.controller.auth_middleware import require_user, require_admin
from app.service.usuarios_service import eliminar, listar, obtener, editar

usuarios_bp = Blueprint("usuarios", __name__)

"""
Controlador de usuarios para la API de Flask.
Este módulo define las rutas relacionadas con la gestión de usuarios, incluyendo operaciones de listado, obtención, edición y eliminación de usuarios. Utiliza middlewares para requerir autenticación y autorización de administrador en ciertas rutas.
Rutas:
- GET /usuarios: Lista todos los usuarios (requiere admin).
- GET /usuarios/me: Obtiene la información del usuario autenticado.
- GET /usuarios/<int:id>: Obtiene la información de un usuario por ID (requiere admin).
- PUT /usuarios/<int:id>: Modifica los datos de un usuario por ID.
- PUT /usuarios/me: Permite al usuario autenticado modificar su propio perfil.
- DELETE /usuarios/<int:id>: Elimina (inhabilita) un usuario por ID.
Manejo de errores:
- Devuelve mensajes de error claros en caso de errores de validación, valores incorrectos o errores internos del servidor.
Dependencias:
- Flask: Para la gestión de rutas y solicitudes HTTP.
- Pydantic: Para la validación de datos.
- auth_middleware: Middlewares de autenticación y autorización.
- usuarios_service: Lógica de negocio para operaciones sobre usuarios.
"""

# Listar todos los usuarios
@usuarios_bp.route("/usuarios", methods=["GET"])
@require_admin
def get():
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        return jsonify(listar(L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@usuarios_bp.route("/usuarios/me", methods=["GET"])
@require_user
def get_me():
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        if 'id_usuario' not in request.json: return ValueError({"error":"Falta el campo 'id_usuario' en la solicitud"}),400
        return jsonify(obtener(request.id_usuario)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
@require_admin
def get_by_id(id):
    try:
        return jsonify(obtener(id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar usuario, este metodo permite cambiar los datos de un usuario existente. antes
# de utilizarlo se supone que se comprobo la contraseña
@usuarios_bp.route('/usuarios/<int:id>', methods=["PUT"])
def put(id):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        editar(id, request.json, admin=True)
        return jsonify({"message":"Usuario modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@usuarios_bp.route("/usuarios/me", methods=["PUT"])
@require_user
def update_me():
    try:
        editar(request.user_id, request.json, admin=False)
        return jsonify({"message": "Perfil actualizado"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar usuario (cambiar su estado a inactivo)
@usuarios_bp.route('/usuarios/<int:id>', methods=["DELETE"])
def dalete(id):
    try:
        return jsonify(eliminar(id, by_id=True)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500