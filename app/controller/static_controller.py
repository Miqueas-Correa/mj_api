from flask import Blueprint, send_from_directory
import os

static_bp = Blueprint("static", __name__)

# Ruta base de uploads
UPLOAD_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')

@static_bp.route('/uploads/<path:subpath>', methods=['GET'])
def serve_upload(subpath):
    try:
        # subpath será algo como: productos/imagen_123.jpg
        return send_from_directory(UPLOAD_BASE, subpath)
    except FileNotFoundError:
        return {'error': 'Archivo no encontrado'}, 404
    except Exception as e:
        return {'error': 'Error al cargar el archivo'}, 500