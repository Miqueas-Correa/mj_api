from flask import Flask
from model.usuarios_model import db
from controller.usuarios_controller import usuarios_bp
from config import Config

app = Flask(__name__)

# Cargar configuración desde config.py
app.config.from_object(Config)

# Inicializar la DB
db.init_app(app)

# Registrar rutas
app.register_blueprint(usuarios_bp)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
