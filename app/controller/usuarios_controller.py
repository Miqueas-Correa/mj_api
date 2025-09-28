from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from service.usuarios_service import usuario_nuevo
from model.usuarios_model import db, Usuario
from model.dto.UsuarioDTO import UsuarioEntradaDTO, UsuarioSalidaDTO

usuarios_bp = Blueprint("usuarios", __name__)

# Listar usuarios
@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    # .query es el acceso al constructor de consultas de SQLAlchemy (Query object).
    # .all() ejecuta la consulta SELECT * FROM usuarios y devuelve una lista de instancias del modelo Usuario.
    # Tipo devuelto: List[Usuario] (cada elemento es un objeto con atributos como id, nombre, email, contrasenia, telefono, activo, rol).
    usuarios = Usuario.query.all()
    print(usuarios)
    # filtro los datos sensibles (contrasenia) y convierto a dict
    return jsonify([UsuarioSalidaDTO.from_model(u).__dict__ for u in usuarios]), 200


# !get usuario por query params
# @usuarios_bp.route("/usuarios/buscar", methods=["GET"])

# Crear usuario
@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    if not request.is_json: return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
    try:
        # valido y creo el usuario
        db.session.add(usuario_nuevo(UsuarioEntradaDTO(**request.json))) # prepara la insercion
        db.session.commit() # ejecuta la insercion en la base de datos
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    return jsonify({"message": "Usuario creado exitosamente"}), 201

# @usuarios_bp.route('/usuarios/<int:id_usuario>', methods=["PUT"])
# def modificar_usuario_json(id_usuario):
#     if request.is_json:
#         if "nombre_de_usuario" in request.json and "contraseña" in request.json:
#             usuario = request.get_json()
#             usuario_modificado=editar_usuario_por_id(id_usuario,usuario["nombre_de_usuario"], usuario["contraseña"])
#             return jsonify(usuario_modificado),200
#         else:
#             return jsonify({"error":"Faltan datos"}),400
#     else:
#         return jsonify({"error":"El formato de la solicitud no es JSON"}),400
    
# @usuarios_bp.route('/usuarios/<int:id_usuario>', methods=["DELETE"])
# def eliminar_usuario_json(id_usuario):
#     return jsonify(eliminar_usuario_por_id(id_usuario)),200