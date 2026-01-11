from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError
from app.service.pedidos_service import editar
from app.service.usuarios_service import obtener
"""
Controlador de usuarios para la API.
Rutas:
    GET /usuarios/me:
        Obtiene la información del usuario autenticado.
        Requiere autenticación JWT.
        Respuestas:
            200: Información del usuario en formato JSON.
            404: Usuario no encontrado.
            500: Error interno del servidor.
    PUT /usuarios/me:
        Actualiza el perfil del usuario autenticado.
        Requiere autenticación JWT.
        Cuerpo de la solicitud: JSON con los datos a actualizar.
        Respuestas:
            200: Perfil actualizado exitosamente.
            400: Error de validación o datos incorrectos.
            500: Error interno del servidor.
"""

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios/me", methods=["GET"])
@jwt_required()
def get_me():
    try:
        return jsonify(obtener(int(get_jwt_identity()))), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500



@usuarios_bp.route("/usuarios/me", methods=["PUT"])
@jwt_required()
def update_me():
    try:
        user_id = get_jwt_identity()
        editar(user_id, request.json, es_admin=False)
        return jsonify({"message": "Perfil actualizado"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500