from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.service.usuarios_service import check_password, eliminar, listar, obtener_U, crear, editar

usuarios_bp = Blueprint("usuarios", __name__)


"""
Controlador de usuarios para la API de Flask.
Este módulo define las rutas relacionadas con la gestión de usuarios, incluyendo operaciones para listar, buscar, crear, modificar, comprobar contraseñas y eliminar usuarios. Utiliza servicios definidos en `usuarios_service` para la lógica de negocio y maneja errores comunes devolviendo respuestas JSON apropiadas.
Rutas:
- GET    /usuarios                      : Lista todos los usuarios, con opción de filtrar por activos.
- GET    /usuarios/<string:nombre>      : Obtiene un usuario por su nombre.
- GET    /usuarios/<int:id>             : Obtiene un usuario por su ID.
- POST   /usuarios                      : Crea un nuevo usuario.
- POST   /usuarios/comprobar/<string:nombre> : Comprueba la contraseña de un usuario por nombre.
- POST   /usuarios/comprobar/<int:id>        : Comprueba la contraseña de un usuario por ID.
- PUT    /usuarios/<int:id>             : Modifica los datos de un usuario por ID.
- PUT    /usuarios/<string:nombre>      : Modifica los datos de un usuario por nombre.
- DELETE /usuarios/<int:id>             : Elimina (inhabilita) un usuario por ID.
- DELETE /usuarios/<string:nombre>      : Elimina (inhabilita) un usuario por nombre.
Manejo de errores:
- Devuelve errores de validación, errores de datos faltantes o incorrectos, y errores internos del servidor en formato JSON.
Dependencias:
- Flask (Blueprint, request, jsonify)
- Pydantic (ValidationError)
- app.service.usuarios_service (check_password, eliminar, listar, obtener_U, crear, editar)
"""

# Listar todos los usuarios
@usuarios_bp.route("/usuarios", methods=["GET"])
def get():
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        # filtro los datos sensibles (contrasenia) y convierto a dict
        return jsonify(listar(L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar usuario por id
@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
def get_id(id):
    try:
        return jsonify(obtener_U(True, id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar usuario, este metodo permite cambiar los datos de un usuario existente. antes
# de utilizarlo se supone que se comprobo la contraseña
@usuarios_bp.route('/usuarios/<int:id>', methods=["PUT"])
def put_id(id):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        # reviso si el usuario existe y si la contraseña es correcta
        editar(id, request.json, by_id=True)
        return jsonify({"message":"Usuario modificado exitosamente"}),200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar usuario (cambiar su estado a inactivo)
@usuarios_bp.route('/usuarios/<int:id>', methods=["DELETE"])
def dalete_id(id):
    try:
        return jsonify(eliminar(id, by_id=True)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500