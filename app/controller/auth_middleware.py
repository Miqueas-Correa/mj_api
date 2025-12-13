from flask import request, jsonify
import jwt
from app.config import Config
from functools import wraps

# Autenticación middleware: requiere token JWT válido, se ejecuta antes de la función decorada
def require_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Falta token"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]

        except Exception:
            return jsonify({"message": "Token inválido o expirado"}), 401

        return function(*args, **kwargs)
    return wrapper