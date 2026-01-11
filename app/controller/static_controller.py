from flask import Blueprint, send_from_directory
import os
"""
Controlador para servir archivos estáticos subidos por los usuarios.
Este módulo define un Blueprint de Flask para manejar la entrega de archivos ubicados en la carpeta 'static/uploads'.
Incluye una ruta para acceder a archivos dentro de subdirectorios específicos, como imágenes de productos.
Atributos:
    static_bp (Blueprint): Blueprint de Flask para rutas estáticas.
    UPLOAD_BASE (str): Ruta base absoluta donde se almacenan los archivos subidos.
Rutas:
    /uploads/<path:subpath> (GET): Sirve archivos desde la carpeta de uploads. 
        Parámetros:
            subpath (str): Ruta relativa dentro de 'uploads' del archivo solicitado.
        Respuestas:
            200: Devuelve el archivo solicitado.
            404: Archivo no encontrado.
            500: Error interno al cargar el archivo.
"""

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