import pytest
from app.app import create_app
from app.model.dto.UsuariosDTO import validar_telefono_ar
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.model.productos_model import Producto
from app.model.usuarios_model import db, Usuario
from werkzeug.security import generate_password_hash
"""
Este módulo define fixtures de pytest para pruebas unitarias en la aplicación Flask.
Clases:
    TestingConfig: Configuración de prueba para la base de datos y la aplicación.
Fixtures:
    app:
        Crea una instancia de la aplicación Flask con configuración de prueba.
        Inicializa y elimina la base de datos en memoria antes y después de cada test.
    app_context:
        Proporciona un contexto de aplicación para cada test, asegurando el correcto manejo de recursos.
    sample_user:
        Crea y retorna un usuario de ejemplo en la base de datos para pruebas relacionadas a usuarios.
    sample_product:
        Crea y retorna un producto de ejemplo en la base de datos para pruebas relacionadas a productos.
    sample_pedido:
        Crea y retorna un pedido de ejemplo, asociado a un usuario y un producto, para pruebas relacionadas a pedidos.
"""

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
    # Crea y limpia el contexto de aplicación para cada test
    with app.app_context():
        yield

# USUARIOS
@pytest.fixture
def sample_user(app):
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

# PRODUCTOS
@pytest.fixture(scope="function")
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

# PEDIDOS
@pytest.fixture
def sample_pedido(app_context, sample_user, sample_product):
    pedido = Pedido(id_usuario=sample_user.id, total=100)
    detalle = PedidoDetalle(producto_id=sample_product.id, cantidad=1)
    pedido.detalles.append(detalle)
    db.session.add(pedido)
    db.session.commit()
    return pedido