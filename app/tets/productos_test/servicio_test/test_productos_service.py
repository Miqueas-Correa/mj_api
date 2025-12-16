import pytest
from app.service.productos_service import (
    categorias_list, featured, listar, obtener, crear, editar, eliminar
)
from app.model.productos_model import db, Producto

# ------------------------
# TEST listar()
# ------------------------

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

# ------------------------
# TEST obtener()
# ------------------------

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

# ------------------------
# TEST categorias_list()
# ------------------------

def test_categorias_list_success(app_context):
    p1 = Producto(
        nombre="Prod1", precio=10, stock=5,
        categoria="Ropa", descripcion="d1",
        imagen_url="url", mostrar=True
    )
    p2 = Producto(
        nombre="Prod2", precio=20, stock=3,
        categoria="Electrónica", descripcion="d2",
        imagen_url="url", mostrar=True
    )
    p3 = Producto(
        nombre="Prod3", precio=30, stock=1,
        categoria="Ropa", descripcion="d3",
        imagen_url="url", mostrar=True
    )

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    result = categorias_list()
    assert set(result) == {"Ropa", "Electrónica"}

def test_categorias_list_empty(app_context):
    Producto.query.delete()
    db.session.commit()

    result = categorias_list()
    assert result == []

def test_categorias_list_exception(app_context, monkeypatch):
    def fake_query_fail(*args, **kwargs):
        raise Exception("DB ERROR")

    monkeypatch.setattr(db.session, "query", fake_query_fail)

    with pytest.raises(ValueError, match="Error al listar categorías"):
        categorias_list()

# ------------------------
# TEST featured()
# ------------------------

def test_featured_no_filter(app_context):
    p1 = Producto(nombre="A", precio=1, stock=1, categoria="X",
                  descripcion="d1", imagen_url="img", mostrar=True, destacado=True)
    p2 = Producto(nombre="B", precio=1, stock=1, categoria="X",
                  descripcion="d2", imagen_url="img", mostrar=False, destacado=True)

    db.session.add_all([p1, p2])
    db.session.commit()

    result = featured(None)
    assert len(result) == 2

def test_featured_mostrar_true(app_context):
    p1 = Producto(nombre="A", precio=1, stock=1, categoria="X",
                  descripcion="d1", imagen_url="img", mostrar=True, destacado=True)
    p2 = Producto(nombre="B", precio=1, stock=1, categoria="X",
                  descripcion="d2", imagen_url="img", mostrar=False, destacado=True)

    db.session.add_all([p1, p2])
    db.session.commit()

    result = featured("true")
    assert len(result) == 1
    assert result[0]["nombre"] == "A"

def test_featured_mostrar_false(app_context):
    p1 = Producto(nombre="A", precio=1, stock=1, categoria="X",
                  descripcion="d1", imagen_url="img", mostrar=True, destacado=True)
    p2 = Producto(nombre="B", precio=1, stock=1, categoria="X",
                  descripcion="d2", imagen_url="img", mostrar=False, destacado=True)

    db.session.add_all([p1, p2])
    db.session.commit()

    result = featured("false")
    assert len(result) == 1
    assert result[0]["nombre"] == "B"

def test_featured_invalid_param(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'mostrar'"):
        featured("asdsad")

# ------------------------
# TEST crear()
# ------------------------

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
    assert float(p.precio) == 50.0

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

# ------------------------
# TEST editar()
# ------------------------

def test_editar_ok(app_context, sample_product):
    editar(sample_product.id, {"precio": 150, "stock": 20})
    p = db.session.get(Producto, sample_product.id)

    assert float(p.precio) == 150
    assert p.stock == 20

def test_editar_producto_no_encontrado(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        editar(999, {"precio": 1})

def test_editar_campo_invalido(app_context, sample_product):
    with pytest.raises(ValueError, match="no existe en Producto"):
        editar(sample_product.id, {"campo": "valor"})

def test_editar_precio_negativo(app_context, sample_product):
    with pytest.raises(ValueError, match="Error de validación"):
        editar(sample_product.id, {"precio": -10})

def test_editar_stock_negativo(app_context, sample_product):
    with pytest.raises(ValueError, match="Error de validación"):
        editar(sample_product.id, {"stock": -5})

# ------------------------
# TEST eliminar()
# ------------------------

def test_eliminar_ok(app_context, sample_product):
    res = eliminar(sample_product.id)
    assert res["message"] == "Producto eliminado exitosamente"
    assert db.session.get(Producto, sample_product.id) is None

def test_eliminar_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        eliminar(999)