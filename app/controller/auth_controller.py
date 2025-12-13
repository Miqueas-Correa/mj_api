from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from pydantic import ValidationError
from app.service.usuarios_service import check_password, crear

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400

    try:
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        email = request.json.get("email") if "email" in request.json else None

        if not email or not contrasenia: return jsonify({"error": "Email y contraseña requeridos"}), 400

        data = check_password(email, contrasenia)

        return jsonify({
            "message": "Contraseña correcta",
            "token": data["token"],
            "usuario": data["usuario"]
        }), 200

    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400

    try:
        crear(request.json)

        return jsonify({"message": "Usuario creado exitosamente"}), 201

    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logout OK"}), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    return jsonify({"token": new_token}), 200