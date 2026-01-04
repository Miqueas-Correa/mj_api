from tkinter import Image
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.controller.auth_middleware import require_admin
from app.service.admin_service import (
    crear_producto, editar_pedido, editar_producto, editar_usuario,
    eliminar_pedido, eliminar_producto, eliminar_usuario, listar_pedidos,
    listar_productos, listar_usuarios, obtener_pedido, obtener_productos,
    obtener_usuario
)
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

"""
    PRODUCTOS
"""

# ✅ Configuración de subida de archivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads', 'productos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGE_DIMENSION = 2000  # píxeles

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_stream):
    """
    Valida que el archivo sea realmente una imagen y no un archivo malicioso.
    """
    try:
        img = Image.open(file_stream)
        img.verify()  # Verifica que sea una imagen válida
        file_stream.seek(0)  # Resetear el puntero del archivo
        return True
    except Exception:
        return False

def resize_image_if_needed(filepath, max_dimension=MAX_IMAGE_DIMENSION):
    try:
        with Image.open(filepath) as img:
            # Convertir RGBA a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Redimensionar si es necesario
            if img.width > max_dimension or img.height > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=85)
    except Exception as e:
        print(f"⚠️ Error redimensionando imagen: {str(e)}")

def get_base_url():
    # Intenta obtener de la configuración
    base_url = current_app.config.get('BACKEND_URL')

    if not base_url:
        # Fallback: construir desde el request
        if request.host.startswith('localhost') or request.host.startswith('127.0.0.1'):
            base_url = f"{request.scheme}://{request.host}"
        else:
            # En producción, usar la URL configurada o construirla
            base_url = f"{request.scheme}://{request.host}"

    return base_url

# Ruta para subir imágenes con todas las validaciones
@admin_bp.route('/upload-image', methods=['POST'])
@jwt_required()
@require_admin
def upload_image_endpoint():
    try:
        # Validar que se envió un archivo
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400

        file = request.files['image']
        filename = request.form.get('filename')

        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

        # Validar tamaño del archivo
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            return jsonify({
                'error': f'El archivo es demasiado grande. Máximo {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 400

        # Validar extensión
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Tipo de archivo no permitido. Solo: ' + ', '.join(ALLOWED_EXTENSIONS)
            }), 400

        # Validar que sea realmente una imagen
        if not validate_image(file.stream):
            return jsonify({'error': 'El archivo no es una imagen válida'}), 400

        # Asegurar que la carpeta existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Verificar si el archivo ya existe y generar uno nuevo si es necesario
        base_filename = filename
        counter = 1
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        while os.path.exists(filepath):
            name, ext = os.path.splitext(base_filename)
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1

        # Guardar el archivo
        file.save(filepath)

        # Optimizar/redimensionar la imagen
        resize_image_if_needed(filepath)

        base_url = get_base_url()
        image_url = f'{base_url}/uploads/productos/{filename}'

        return jsonify({'url': image_url}), 200
    except Exception as e:
        return jsonify({'error': 'Error al subir la imagen', 'detalle': str(e)}), 500

# Ruta para eliminar imágenes (opcional pero recomendado)
@admin_bp.route('/delete-image', methods=['DELETE'])
@jwt_required()
@require_admin
def delete_image_endpoint():
    try:
        filename = request.json.get('filename')

        if not filename:
            return jsonify({'error': 'No se especificó el nombre del archivo'}), 400

        # Extraer solo el nombre del archivo de la URL completa si viene así
        if 'uploads/productos/' in filename:
            filename = filename.split('uploads/productos/')[-1]

        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Verificar que el archivo existe
        if not os.path.exists(filepath):
            return jsonify({'error': 'Imagen no encontrada'}), 404

        # Verificar que está dentro de la carpeta permitida (seguridad)
        if not os.path.abspath(filepath).startswith(os.path.abspath(UPLOAD_FOLDER)):
            return jsonify({'error': 'Operación no permitida'}), 403

        # Eliminar el archivo
        os.remove(filepath)
        return jsonify({'message': 'Imagen eliminada exitosamente'}), 200
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
        return jsonify(obtener_productos(2, categoria)), 200
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
        editar_usuario(id, request.json, es_admin=True)
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