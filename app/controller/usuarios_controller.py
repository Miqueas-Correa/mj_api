from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from service.usuarios_service import check_password, eliminar_usuario_service, listar_usuarios_service, obtener_usuario, usuario_nuevo, editar_usuario
from model.usuarios_model import Usuario
from model.dto.UsuarioDTO import UsuarioEntradaDTO, UsuarioSalidaDTO, UsuarioUpdateDTO

usuarios_bp = Blueprint("usuarios", __name__)

# Listar todos los usuarios
@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        # filtro los datos sensibles (contrasenia) y convierto a dict
        return jsonify(listar_usuarios_service(L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# buscar usuario por nombre
@usuarios_bp.route("/usuarios/<string:nombre>", methods=["GET"])
def obtener_usuario_por_nombre(nombre):
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        return jsonify(obtener_usuario(False, nombre, L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# buscar usuario por id
@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario_por_id(id):
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        return jsonify(obtener_usuario(True, id, L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# Crear usuario
@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
    try:
        # valido y creo el usuario
        usuario_nuevo(UsuarioEntradaDTO(**request.json))
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

# comprobar contraseña nombre
@usuarios_bp.route("/usuarios/comprobar/<string:nombre>", methods=["POST"])
def comprobar_contrasenia(nombre):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400

    try:
        # valido y compruebo la contraseña
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        if contrasenia is None: return jsonify({"error":"Faltan datos"}),400
        check_password(nombre, contrasenia, by_id=False)
        return jsonify({"message": "Contraseña correcta"}), 200
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400

# comprobar contraseña id
@usuarios_bp.route("/usuarios/comprobar/<int:id>", methods=["POST"])
def comprobar_contrasenia_id(id):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400

    try:
        # valido y compruebo la contraseña
        contrasenia = request.json.get("contrasenia") if "contrasenia" in request.json else None
        if contrasenia is None: return jsonify({"error":"Faltan datos"}),400
        check_password(id, contrasenia, by_id=True)
        return jsonify({"message": "Contraseña correcta"}), 200
    except ValueError as e:
        return jsonify({"errors": str(e)}), 400

# Modificar usuario, este metodo permite cambiar los datos de un usuario existente. antes
# de utilizarlo se supone que se comprobo la contraseña
@usuarios_bp.route('/usuarios/<int:id>', methods=["PUT"])
def modificar_usuario(id):
    if not request.is_json: return jsonify({"error":"El formato de la solicitud no es JSON"}),400

    try:
        # reviso si el usuario existe y si la contraseña es correcta
        editar_usuario(id, UsuarioUpdateDTO(**request.json))
        return jsonify({"message":"Usuario modificado exitosamente"}),200
    except ValueError as e:
        return jsonify({"error": e.errors()}),404

# Eliminar usuario (cambiar su estado a inactivo)
@usuarios_bp.route('/usuarios/<int:id>', methods=["DELETE"])
def eliminar_usuario_json(id):
    return jsonify(eliminar_usuario_service(id)),200

@usuarios_bp.route("/usuarios/<string:nombre>", methods=["DELETE"])
def eliminar_usuario_nombre(nombre):
    return jsonify(eliminar_usuario_service(nombre, by_id=False)),200