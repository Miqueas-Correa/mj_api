from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from functools import wraps

"""
Este módulo proporciona middlewares de autenticación para rutas protegidas en una aplicación Flask utilizando JWT.
Funciones:
    require_admin(fn): Decorador que restringe el acceso a la ruta solo a usuarios con el rol de administrador. 
                      Si el usuario no es administrador, retorna un mensaje de error y un código de estado 403.
"""

def require_admin(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("rol") != "admin":
            return jsonify({"message": "Acceso solo para administradores"}), 403
        return fn(*args, **kwargs)
    return wrapper