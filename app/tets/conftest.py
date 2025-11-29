import pytest
from app.app import create_app
from app.model import db
from app.model.usuarios_model import Usuario
from app.model.productos_model import Producto
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.model.dto.UsuariosDTO import validar_telefono_ar
from werkzeug.security import generate_password_hash

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = False
    # asegurar que exista la clave para CORS cuando create_app la lee
    CORS_ORIGINS = ["*"]
    CORS_SUPPORTS_CREDENTIALS = False

@pytest.fixture(scope="session")
def app():
    # NOTA: le paso la CLASE; create_app es tolerante y manejará clase/instancia
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def app_context(app):
    """
    Proporciona contexto de app, crea tablas antes de cada test y las borra luego.
    """
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_user(app_context):
    usuario = Usuario(
        nombre="mike",
        email="mike@test.com",
        telefono=validar_telefono_ar("1123456789"),
        contrasenia=generate_password_hash("1234"),
        activo=True,
        rol="cliente"
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario

@pytest.fixture
def sample_product(app_context):
    producto = Producto(
        nombre="TestProducto",
        precio=100.0,
        stock=10,
        categoria="Categoria1",
        descripcion="Descripción de prueba",
        imagen_url="http://imagen.com/test.jpg",
        mostrar=True
    )
    db.session.add(producto)
    db.session.commit()
    return producto

@pytest.fixture
def sample_pedido(app_context, sample_user, sample_product):
    pedido = Pedido(id_usuario=sample_user.id, total=sample_product.precio)
    detalle = PedidoDetalle(producto_id=sample_product.id, cantidad=1)
    pedido.detalles.append(detalle)
    db.session.add(pedido)
    db.session.commit()
    return pedido