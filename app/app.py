from flask import Flask
from flask_cors import CORS
from app.model import db
from app.controller.pedidos_controller import pedidos_bp
from app.controller.usuarios_controller import usuarios_bp
from app.controller.productos_controller import productos_bp

def _load_config(app, config_like):
    """
    Carga configuración en app.config desde:
    - una clase (Config)
    - una instancia de clase
    - un dict
    - si es None, intenta cargar app.config default (no hace nada)
    """
    if config_like is None:
        return

    # Si es un diccionario, actualizar directamente
    if isinstance(config_like, dict):
        app.config.update(config_like)
        return

    # from_object funciona con clase o instancia; usarlo y capturar errores
    try:
        app.config.from_object(config_like)
        return
    except Exception:
        # si falla, intentar instanciar (por si le pasaron la clase en vez de instancia)
        try:
            app.config.from_object(config_like())
            return
        except Exception:
            # fallback: si tiene __dict__, usarlo
            try:
                app.config.update(vars(config_like))
                return
            except Exception:
                pass

def create_app(config_class=None):
    """
    Crea la app Flask. `config_class` puede ser:
      - la clase Config (p.ej. Config)
      - una instancia Config() (p.ej. TestingConfig())
      - un dict con claves de configuración
      - None (usa defaults dentro de la app)
    """
    app = Flask(__name__)

    # cargar configuración tolerante
    _load_config(app, config_class)

    # Obtener origins de forma segura (evita KeyError)
    origins = app.config.get("CORS_ORIGINS", ["*"])
    # Asegurar que origins sea lista o "*" especial
    if isinstance(origins, str):
        origins = [origins] if origins != "*" else ["*"]

    CORS(
        app,
        supports_credentials=app.config.get("CORS_SUPPORTS_CREDENTIALS", True),
        resources={r"/*": {"origins": origins}}
    )

    # Inicializar DB
    db.init_app(app)

    # Registrar blueprints sólo si existen (evita errores en tests parciales)
    try:
        app.register_blueprint(usuarios_bp)
    except Exception:
        pass
    try:
        app.register_blueprint(pedidos_bp)
    except Exception:
        pass
    try:
        app.register_blueprint(productos_bp)
    except Exception:
        pass

    return app

if __name__ == "__main__":
    # cuando se ejecuta directamente, cargar Config real si existe
    from app.config import Config
    app = create_app(Config)
    app.run(debug=app.config.get("DEBUG", False))
