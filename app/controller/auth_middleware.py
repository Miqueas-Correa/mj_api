from flask import request, jsonify
import jwt
from app.config import Config
from functools import wraps

"""
Este módulo proporciona middlewares de autenticación y autorización para rutas de Flask.
Funciones:
-----------
- require_user(function):
    Decorador que verifica la presencia y validez de un token JWT en la cabecera "Authorization" de la solicitud.
    Si el token es válido, agrega los atributos `user_id` y `user_rol` al objeto `request`.
    Si el token falta, está expirado o es inválido, retorna una respuesta JSON con el mensaje correspondiente y el código de estado HTTP adecuado.
- require_admin(function):
    Decorador que requiere que el usuario autenticado tenga el rol de "admin".
    Utiliza el decorador `require_user` para asegurar que el usuario esté autenticado.
    Si el usuario no es administrador, retorna una respuesta JSON con un mensaje de acceso denegado y código de estado 403.
"""

def require_admin(function):
    @wraps(function)
    @require_user
    def wrapper(*args, **kwargs):
        if request.user_rol != "admin":
            return jsonify({"message": "Acceso solo para administradores"}), 403

        return function(*args, **kwargs)

    return wrapper

def require_user(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Falta token"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user_id = decoded.get("user_id")
            request.user_rol = decoded.get("rol")

            if not request.user_id:
                return jsonify({"message": "Token inválido"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        return function(*args, **kwargs)

    return wrapper