from flask import Flask
from app.model import db
from app.controller.pedidos_controller import pedidos_bp
from app.controller.usuarios_controller import usuarios_bp
from app.controller.productos_controller import productos_bp
from app.config import Config

app = Flask(__name__)

# Cargar configuración desde config.py
app.config.from_object(Config)

# Inicializar la DB
db.init_app(app)

# Registrar rutas
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(productos_bp)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
