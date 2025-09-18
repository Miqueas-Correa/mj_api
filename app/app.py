from flask import Flask
from model.usuarios_model import db_usuarios
from model.pedidos_model import db_pedidos
from model.productos_model import db_productos
from controller.pedidos_controller import pedidos_bp
from controller.usuarios_controller import usuarios_bp
from controller.productos_controller import db_productos
from config import Config

app = Flask(__name__)

# Cargar configuración desde config.py
app.config.from_object(Config)

# Inicializar la DB
db_usuarios.init_app(app)
db_pedidos.init_app(app)
db_productos.init_app(app)

# Registrar rutas
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(db_productos)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
