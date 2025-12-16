from functools import wraps
from flask import jsonify
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt,
    get_jwt_identity
)

def require_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return jsonify({"message": "Token inválido o faltante"}), 401

        # datos disponibles para la request
        jwt_data = get_jwt()
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"message": "Token inválido"}), 401

        # los inyecto en kwargs para no tocar request global
        kwargs["user_id"] = user_id
        kwargs["user_rol"] = jwt_data.get("rol")

        return fn(*args, **kwargs)

    return wrapper


def require_admin(fn):
    @wraps(fn)
    @require_user
    def wrapper(*args, **kwargs):
        if kwargs.get("user_rol") != "admin":
            return jsonify({"message": "Acceso solo para administradores"}), 403

        return fn(*args, **kwargs)

    return wrapper