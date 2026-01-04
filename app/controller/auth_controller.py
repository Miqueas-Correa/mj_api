from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    get_jwt_identity
)
from pydantic import ValidationError
from app.service.usuarios_service import check_password, crear, logout_token, obtener

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json: 
        return jsonify({"error":"El formato de la solicitud no es JSON"}), 400

    try:
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        email = request.json.get("email") if "email" in request.json else None

        if not email or not contrasenia: 
            return jsonify({"error": "Email y contraseña requeridos"}), 400

        data = check_password(email, contrasenia)

        return jsonify({
            "token": data["token"],
            "refresh": data["refresh"]
        }), 200

    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json: 
        return jsonify({"error":"El formato de la solicitud no es JSON"}), 400

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
    jti = get_jwt()["jti"]
    logout_token(jti)
    return jsonify({"message": "Logout OK"}), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    old_jti = get_jwt()["jti"]
    logout_token(old_jti)

    user_id = get_jwt_identity()
    claims = get_jwt()

    rol = claims.get("rol")

    if not rol:
        try:
            usuario_data = obtener(int(user_id))
            rol = usuario_data.get("rol", "cliente")
        except Exception:
            rol = "cliente"

    access = create_access_token(
        identity=user_id,
        additional_claims={"rol": rol}
    )

    refresh = create_refresh_token(
        identity=user_id,
        additional_claims={"rol": rol}
    )

    return jsonify({
        "token": access,
        "refresh": refresh
    }), 200