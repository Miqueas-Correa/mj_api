import pytest
from app.service.productos_service import (
    categorias_list, featured, listar, obtener
)
from app.model.productos_model import db, Producto

# ------------------------
# TEST listar()
# ------------------------

def test_listar_todos(app_context, sample_product):
    res = listar()
    assert len(res) >= 1
    # Solo muestra productos con mostrar=True
    assert all(p["mostrar"] is True for p in res)

# ------------------------
# TEST obtener()
# ------------------------

def test_obtener_por_id(app_context, sample_product):
    res = obtener(1, sample_product.id)
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_por_nombre(app_context, sample_product):
    res = obtener(0, "Test")
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_por_categoria(app_context, sample_product):
    res = obtener(2, "Categoria1")
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto 999 no fue encontrado"):
        obtener(1, 999)

def test_obtener_by_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'by'"):
        obtener(3, 1)

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

def test_featured_ok(app_context):
    p1 = Producto(nombre="A", precio=1, stock=1, categoria="X",
                  descripcion="d1", imagen_url="img", mostrar=True, destacado=True)
    p2 = Producto(nombre="B", precio=1, stock=1, categoria="X",
                  descripcion="d2", imagen_url="img", mostrar=False, destacado=True)

    db.session.add_all([p1, p2])
    db.session.commit()

    result = featured()
    # Solo retorna los que tienen mostrar=True
    assert len(result) == 1
    assert result[0]["nombre"] == "A"