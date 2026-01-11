from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps
"""
Este módulo proporciona un decorador para restringir el acceso a rutas solo a usuarios con rol de administrador.
Funciones:
    require_admin(fn): Decorador que verifica si el usuario autenticado tiene el rol de 'admin' en sus claims JWT.
    Si no es administrador, retorna un mensaje de error y un código de estado 403.
"""

def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("rol") != "admin":
            return jsonify({"message": "Acceso solo para administradores"}), 403
        return fn(*args, **kwargs)
    return wrapper