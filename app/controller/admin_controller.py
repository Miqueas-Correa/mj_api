from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.controller.auth_middleware import require_admin
from app.service.admin_service import (
    crear_producto, editar_pedido, editar_producto, editar_usuario,
    eliminar_pedido, eliminar_producto, eliminar_usuario, listar_pedidos,
    listar_productos, listar_usuarios, obtener_pedido, obtener_productos,
    obtener_usuario
)
from app.service.cloudinary_service import upload_image, delete_image

"""
Controlador de rutas administrativas para la gestión de productos, usuarios y pedidos en la API.
Incluye:
- Subida y eliminación de imágenes de productos en Cloudinary.
- CRUD completo para productos: listar, buscar (por nombre, id, categoría), crear, modificar y eliminar.
- CRUD para usuarios: listar, obtener por id, modificar (rol y estado), y eliminar (cambio de estado a inactivo).
- CRUD para pedidos: listar, buscar (por usuario, id, código de producto), modificar y eliminar.

Todas las rutas están protegidas por autenticación JWT y requieren permisos de administrador.
"""

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

"""
    PRODUCTOS
"""

# Configuración
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para subir imágenes a Cloudinary
@admin_bp.route('/upload-image', methods=['POST'])
@jwt_required()
@require_admin
def upload_image_endpoint():
    try:
        # Validar que se envió un archivo
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

        # Validar tamaño del archivo
        file.seek(0, 2)  # Seek to end
        file_length = file.tell()
        file.seek(0)  # Reset to beginning

        if file_length > MAX_FILE_SIZE:
            return jsonify({
                'error': f'El archivo es demasiado grande. Máximo {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 400

        # Validar extensión
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Tipo de archivo no permitido. Solo: ' + ', '.join(ALLOWED_EXTENSIONS)
            }), 400

        # Subir a Cloudinary
        image_url = upload_image(file, folder="productos")

        return jsonify({'url': image_url}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al subir la imagen', 'detalle': str(e)}), 500

# Ruta para eliminar imágenes de Cloudinary
@admin_bp.route('/delete-image', methods=['DELETE'])
@jwt_required()
@require_admin
def delete_image_endpoint():
    try:
        image_url = request.json.get('url')

        if not image_url:
            return jsonify({'error': 'No se especificó la URL de la imagen'}), 400

        # Eliminar de Cloudinary
        success = delete_image(image_url)
        
        if success:
            return jsonify({'message': 'Imagen eliminada exitosamente'}), 200
        else:
            return jsonify({'error': 'No se pudo eliminar la imagen'}), 400
            
    except Exception as e:
        return jsonify({'error': 'Error al eliminar la imagen', 'detalle': str(e)}), 500

# Listar Productos
@admin_bp.route("/productos", methods=["GET"])
@jwt_required()
@require_admin
def get_productos():
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(listar_productos(L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por nombre
@admin_bp.route("/productos/<string:nombre>", methods=["GET"])
@jwt_required()
@require_admin
def get_producto_by_name(nombre):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_productos(0, nombre, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por id
@admin_bp.route("/productos/<int:id>", methods=["GET"])
@jwt_required()
@require_admin
def get_producto_by_id(id):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_productos(1, id, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar producto por categoria
@admin_bp.route("/productos/categoria/<string:categoria>", methods=["GET"])
@jwt_required()
@require_admin
def get_producto_by_category(categoria):
    try:
        L_mostrar = request.args.get("mostrar", default=None, type=str)
        return jsonify(obtener_productos(2, categoria, L_mostrar)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Crear producto
@admin_bp.route("/productos", methods=["POST"])
@jwt_required()
@require_admin
def post_producto():
    try:
        if not request.is_json: 
            return jsonify({"error": "El formato de la solicitud no es JSON"}), 400
        crear_producto(request.json)
        return jsonify({"message": "Producto creado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar producto
@admin_bp.route('/productos/<int:id>', methods=["PUT"])
@jwt_required()
@require_admin
def put_producto(id):
    try:
        if not request.is_json: 
            return jsonify({"error":"El formato de la solicitud no es JSON"}), 400
        editar_producto(id, request.json)
        return jsonify({"message":"Producto modificado exitosamente"}), 200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar producto por id
@admin_bp.route('/productos/<int:id>', methods=["DELETE"])
@jwt_required()
@require_admin
def delete_producto(id):
    try:
        return jsonify(eliminar_producto(id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

"""
    USUARIOS
"""

# Listar todos los usuarios
@admin_bp.route("/usuarios", methods=["GET"])
@jwt_required()
@require_admin
def get_usuarios():
    try:
        L_activos = request.args.get("activos", default=None, type=str)
        return jsonify(listar_usuarios(L_activos)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

@admin_bp.route("/usuarios/<int:id>", methods=["GET"])
@jwt_required()
@require_admin
def get_usuario_by_id(id):
    try:
        return jsonify(obtener_usuario(id)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar usuario
@admin_bp.route('/usuarios/<int:id>', methods=["PUT"])
@jwt_required()
@require_admin
def put_usuario(id):
    if not request.is_json: 
        return jsonify({"error":"El formato de la solicitud no es JSON"}), 400
    try:
        editar_usuario(id, request.json)
        return jsonify({"message":"Usuario modificado exitosamente"}), 200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar usuario (cambiar su estado a inactivo)
@admin_bp.route('/usuarios/<int:id>', methods=["DELETE"])
@jwt_required()
@require_admin
def delete_usuario(id):
    try:
        return jsonify(eliminar_usuario(id, by_id=True)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

"""
    PEDIDOS
"""

# Listar todos los pedidos
@admin_bp.route("/pedidos", methods=["GET"])
@jwt_required()
@require_admin
def get_pedidos():
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(listar_pedidos(L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por id usuario
@admin_bp.route("/pedidos/usuario/<int:id>", methods=["GET"])
@jwt_required()
@require_admin
def get_pedido_by_usuario(id):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener_pedido(0, id, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por id
@admin_bp.route("/pedidos/<int:id>", methods=["GET"])
@jwt_required()
@require_admin
def get_pedido_by_id(id):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener_pedido(1, id, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# buscar pedido por codigo producto
@admin_bp.route("/pedidos/producto/<int:codigo>", methods=["GET"])
@jwt_required()
@require_admin
def get_pedido_by_producto(codigo):
    try:
        L_cerrado = request.args.get("cerrado", default=None, type=str)
        return jsonify(obtener_pedido(2, codigo, L_cerrado)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Modificar pedido
@admin_bp.route('/pedidos/<int:id>', methods=["PUT"])
@jwt_required()
@require_admin
def put_pedido(id):
    try:
        if not request.is_json:
            return jsonify({"error":"El formato de la solicitud no es JSON"}), 400
        editar_pedido(id, request.json)
        return jsonify({"message":"Pedido modificado exitosamente"}), 200
    except ValidationError as e:
        return jsonify({"error": "Error de validación", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

# Eliminar pedido por id
@admin_bp.route('/pedidos/<int:id>', methods=["DELETE"])
@jwt_required()
@require_admin
def delete_pedido(id):
    try:
        eliminar_pedido(id)
        return jsonify({"message":"Pedido eliminado con exito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500