import pytest
from app.app import create_app
from app.extensions import db
from app.model.usuarios_model import Usuario
from app.model.productos_model import Producto
from app.model.dto.Usuarios_dto import validar_telefono_ar
from werkzeug.security import generate_password_hash
from PIL import Image
from pathlib import Path

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    CORS_ORIGINS = ["*"]
    CORS_SUPPORTS_CREDENTIALS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-jwt-secret"

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
        mostrar=True,
        destacado=False
    )
    db.session.add(producto)
    db.session.commit()
    return producto

@pytest.fixture
def sample_pedido(app_context, sample_user, sample_product):
    from app.model.pedidos_model import Pedido, PedidoDetalle
    from app.extensions import db
    
    pedido = Pedido(
        id_usuario=sample_user.id,
        total=sample_product.precio
    )
    detalle = PedidoDetalle(
        producto_id=sample_product.id,
        cantidad=1
    )
    pedido.detalles.append(detalle)

    db.session.add(pedido)
    db.session.commit()
    return pedido

@pytest.fixture
def client(app, app_context):
    return app.test_client()

@pytest.fixture
def disable_jwt_blacklist(app, monkeypatch):
    monkeypatch.setattr(
        app.extensions["jwt"],
        "_token_in_blocklist_callback",
        lambda *_: False
    )

@pytest.fixture
def test_image_file(app):
    from pathlib import Path

    current = Path(__file__).resolve().parent

    # Subir hasta llegar al directorio que contiene 'app'
    while current.name != 'mj_api' and current.parent != current:
        current = current.parent

    # Ahora current debería ser la raíz del proyecto (mj_api)
    upload_path = current / 'static' / 'uploads' / 'productos'
    upload_path.mkdir(parents=True, exist_ok=True)

    filepath = upload_path / 'test_static.jpg'
    img = Image.new('RGB', (50, 50), color='blue')
    img.save(str(filepath), 'JPEG')

    yield 'test_static.jpg'

    # Cleanup
    if filepath.exists():
        filepath.unlink()