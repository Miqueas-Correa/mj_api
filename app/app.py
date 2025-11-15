from flask import Flask
from app.model import db
from app.config import Config
from app.controller.pedidos_controller import pedidos_bp
from app.controller.usuarios_controller import usuarios_bp
from app.controller.productos_controller import productos_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

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
