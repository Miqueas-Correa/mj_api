from app.app import create_app
from app.config import Config
"""
Este módulo inicializa la aplicación WSGI para el proyecto.
Importa la función `create_app` desde el paquete principal de la aplicación y la clase de configuración `Config`.
Luego, crea una instancia de la aplicación utilizando la configuración especificada.
Atributos:
    app (Flask): Instancia de la aplicación Flask configurada para ser utilizada por el servidor WSGI.
"""

app = create_app(Config)