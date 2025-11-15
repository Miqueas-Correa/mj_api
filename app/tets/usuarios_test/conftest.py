import pytest
from app.app import create_app
from app.model.dto.UsuariosDTO import validar_telefono_ar
from app.model.usuarios_model import db, Usuario
from werkzeug.security import generate_password_hash

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = False

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def app_context(app):
    """Crea y limpia el contexto de aplicación para cada test"""
    with app.app_context():
        yield

@pytest.fixture
def sample_user(app):
    user = Usuario(
        nombre="mike",
        email="mike@test.com",
        telefono=validar_telefono_ar("1123456789"),
        contrasenia=generate_password_hash("1234"),
        activo=True,
        rol="cliente"
    )
    db.session.add(user)
    db.session.commit()
    return user