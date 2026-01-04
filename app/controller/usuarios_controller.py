from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError
from app.service.pedidos_service import editar
from app.service.usuarios_service import obtener

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