from flask import Flask
from app.config import Config
from flask_cors import CORS
from app.extensions import db, jwt
from app.controller.pedidos_controller import pedidos_bp
from app.controller.usuarios_controller import usuarios_bp
from app.controller.productos_controller import productos_bp
from app.controller.auth_controller import auth_bp
from app.controller.admin_controller import admin_bp
from app.controller.static_controller import static_bp
from app.security.jwt_callbacks import register_jwt_callbacks
"""
Este módulo define la función principal para crear e inicializar una aplicación Flask con configuración flexible.
Funciones:
- _load_config(app, config_like): Carga la configuración en la app Flask desde un diccionario, clase, instancia o cualquier objeto compatible. Intenta varias estrategias para asegurar la correcta carga de la configuración.
- create_app(config_class=None): Crea y configura una instancia de Flask. Permite pasar la configuración como clase, instancia, diccionario o None. Inicializa extensiones (DB, JWT, CORS) y registra blueprints de controladores si están disponibles.
- Bloque principal: Si el archivo se ejecuta directamente, crea la app usando la clase Config y la ejecuta con el valor de DEBUG definido en la configuración.
Características destacadas:
- Soporte flexible para cargar configuración.
- Inicialización de CORS con orígenes configurables y soporte para credenciales.
- Registro tolerante de blueprints, útil para pruebas parciales.
- Inicialización de extensiones comunes (base de datos, JWT).
"""

def _load_config(app, config_like):
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
        resources={
            r"/*": {"origins": origins},
            r"uploads/*": {"origins": origins}
        },
        allow_headers=["Content-Type", "Authorization"]
    )

    app.config['MAX_CONTENT_LENGTH'] = app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024)

    # Inicializar DB
    db.init_app(app)

    # Inicializar JWT
    jwt.init_app(app)

    register_jwt_callbacks(jwt)

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
    try:
        app.register_blueprint(auth_bp)
    except Exception:
        pass
    try:
        app.register_blueprint(admin_bp)
    except Exception:
        pass
    try:
        app.register_blueprint(static_bp)
    except Exception:
        pass

    return app

# if __name__ == "__main__":
#     # cuando se ejecuta directamente, cargar Config real si existe
#     import os
#     app = create_app(Config)
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=False)