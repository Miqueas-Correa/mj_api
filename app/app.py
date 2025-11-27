from flask import Flask
from flask_cors import CORS
from app.model import db
from app.config import Config
from app.controller.pedidos_controller import pedidos_bp
from app.controller.usuarios_controller import usuarios_bp
from app.controller.productos_controller import productos_bp
"""
Este módulo define la función de fábrica `create_app` para crear e inicializar una instancia de la aplicación Flask,
configurando CORS, la base de datos y registrando los blueprints de los controladores de usuarios, pedidos y productos.
Funciones:
    create_app(config_class=Config): 
        Crea y configura una instancia de Flask utilizando la clase de configuración proporcionada.
        Inicializa la base de datos, configura CORS y registra los blueprints de la aplicación.
Ejecución directa:
    Si el archivo se ejecuta directamente, se crea la aplicación y se inicia el servidor Flask en modo debug.
"""

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    origins = app.config.get("CORS_ORIGINS", ["*"])

    CORS(
        app,
        supports_credentials=app.config["CORS_SUPPORTS_CREDENTIALS"],
        resources={r"/*": {"origins": origins}}
    )

    # Inicializar DB
    db.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(productos_bp)

    return app

if __name__ == "__main__":
    app = create_app(Config)
    app.run(debug=app.config["DEBUG"])
