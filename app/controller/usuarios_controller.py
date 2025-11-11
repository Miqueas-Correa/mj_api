from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.service.usuarios_service import check_password, eliminar, listar, obtener_U, crear, editar

usuarios_bp = Blueprint("usuarios", __name__)

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

# buscar usuario por nombre
@usuarios_bp.route("/usuarios/<string:nombre>", methods=["GET"])
def get_por_nombre(nombre):
    try:
        return jsonify(obtener_U(False, nombre)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
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

# Crear usuario
@usuarios_bp.route("/usuarios", methods=["POST"])
def post():
    if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
    try:
        # valido y creo el usuario
        crear(request.json)
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# comprobar contraseña nombre
@usuarios_bp.route("/usuarios/comprobar/<string:nombre>", methods=["POST"])
def check_password_name(nombre):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        # valido y compruebo la contraseña
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        if contrasenia is None: return jsonify({"error":"Faltan datos"}),400
        check_password(nombre, contrasenia, by_id=False)
        return jsonify({"message": "Contraseña correcta"}), 200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# comprobar contraseña id
@usuarios_bp.route("/usuarios/comprobar/<int:id>", methods=["POST"])
def check_password_id(id):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        # valido y compruebo la contraseña
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        if contrasenia is None: return jsonify({"error":"Faltan datos"}),400
        check_password(id, contrasenia, by_id=True)
        return jsonify({"message": "Contraseña correcta"}), 200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
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

# Modificar usuario, este metodo permite cambiar los datos de un usuario existente. antes
# de utilizarlo se supone que se comprobo la contraseña
@usuarios_bp.route('/usuarios/<string:nombre>', methods=["PUT"])
def put_name(nombre):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    try:
        # reviso si el usuario existe y si la contraseña es correcta
        editar(nombre, request.json, by_id=False)
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

@usuarios_bp.route("/usuarios/<string:nombre>", methods=["DELETE"])
def delete_name(nombre):
    try:
        # elimino el usuario por su nombre
        return jsonify(eliminar(nombre, by_id=False)),200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500