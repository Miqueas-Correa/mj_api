import pytest
from app.service.productos_service import listar, obtener, crear, editar, eliminar
from app.model.productos_model import db, Producto

# TEST listar()
def test_listar_todos(app_context, sample_product):
    res = listar(None)
    assert len(res) == 1
    assert res[0]["nombre"] == "TestProducto"

def test_listar_mostrar_true(app_context, sample_product):
    res = listar("true")
    assert len(res) == 1

def test_listar_mostrar_false(app_context, sample_product):
    sample_product.mostrar = False
    db.session.commit()
    res = listar("false")
    assert len(res) == 1

def test_listar_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'mostrar'"):
        listar("otro")

# TEST obtener()
def test_obtener_por_id(app_context, sample_product):
    res = obtener(1, sample_product.id, None)
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_por_nombre(app_context, sample_product):
    res = obtener(0, "Test", None)
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_por_categoria(app_context, sample_product):
    res = obtener(2, "Categoria1", None)
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto 999 no fue encontrado"):
        obtener(1, 999, None)

def test_obtener_by_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'by'"):
        obtener(3, 1, None)

# TEST crear()
def test_crear_ok(app_context):
    data = {
        "nombre": "NuevoProducto",
        "precio": 50.0,
        "stock": 5,
        "categoria": "Categoria2",
        "descripcion": "Nuevo producto",
        "imagen_url": "http://imagen.com/nuevo.jpg",
        "mostrar": True
    }
    crear(data)
    p = Producto.query.filter_by(nombre="NuevoProducto").first()
    assert p is not None
    assert p.precio == 50.0

def test_crear_nombre_repetido(app_context, sample_product):
    data = {
        "nombre": "TestProducto",
        "precio": 200,
        "stock": 2,
        "categoria": "Otra",
        "descripcion": "Desc",
        "imagen_url": "url",
        "mostrar": True
    }
    with pytest.raises(ValueError, match="Ya existe un producto con ese nombre"):
        crear(data)

# TEST editar()
def test_editar_ok(app_context, sample_product):
    editar(sample_product.id, {"precio": 150, "stock": 20}, True)
    p = db.session.get(Producto, sample_product.id)
    assert p.precio == 150
    assert p.stock == 20

def test_editar_producto_no_encontrado(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        editar(999, {"precio": 1}, True)

def test_editar_campo_invalido(app_context, sample_product):
    with pytest.raises(ValueError, match="no existe en Producto"):
        editar(sample_product.id, {"campo": "valor"}, True)

def test_editar_precio_negativo(app_context, sample_product):
    with pytest.raises(ValueError, match="Error de validación"):
        editar(sample_product.id, {"precio": -10}, True)

def test_editar_stock_negativo(app_context, sample_product):
    with pytest.raises(ValueError, match="Error de validación"):
        editar(sample_product.id, {"stock": -5}, True)

# TEST eliminar()
def test_eliminar_ok(app_context, sample_product):
    res = eliminar(sample_product.id, True)
    assert res["message"] == "Producto eliminado exitosamente"
    assert db.session.get(Producto, sample_product.id) is None

def test_eliminar_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        eliminar(999, True)