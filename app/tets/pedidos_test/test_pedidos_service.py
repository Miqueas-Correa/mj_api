import pytest
from app.model.pedidos_model import Pedido
from app.extensions import db
from app.service.pedidos_service import crear, editar, eliminar, obtener

# ------------------------
# Tests obtener()
# ------------------------

def test_obtener_por_id(app_context, sample_pedido):
    res = obtener(1, sample_pedido.id, None)
    assert res[0]["id"] == sample_pedido.id

def test_obtener_por_usuario(app_context, sample_user, sample_pedido):
    res = obtener(0, sample_user.id, None)
    assert res[0]["id_usuario"] == sample_user.id

def test_obtener_por_producto(app_context, sample_product, sample_pedido):
    res = obtener(2, sample_product.id, None)
    assert res[0]["detalles"][0]["producto_id"] == sample_product.id

def test_obtener_no_existe(app_context):
    with pytest.raises(ValueError, match="Pedido 999 no encontrado"):
        obtener(1, 999, None)

def test_obtener_by_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'by'"):
        obtener(3, 1, None)

# ------------------------
# Tests crear()
# ------------------------

def test_crear_ok(app_context, sample_user, sample_product):
    data = {
        "id_usuario": sample_user.id,
        "productos": [{"producto_id": sample_product.id, "cantidad": 2}]
    }

    crear(data)

    pedido = (
        Pedido.query
        .filter_by(id_usuario=sample_user.id)
        .order_by(Pedido.id.desc())
        .first()
    )

    assert pedido.total == sample_product.precio * 2
    assert len(pedido.detalles) == 1

def test_crear_producto_invalido(app_context, sample_user):
    data = {
        "id_usuario": sample_user.id,
        "productos": [{"producto_id": 999, "cantidad": 1}]
    }

    with pytest.raises(ValueError, match="Producto 999 no encontrado"):
        crear(data)

# ------------------------
# Tests editar()
# ------------------------

def test_editar_cerrado(app_context, sample_pedido):
    editar(sample_pedido.id, {"cerrado": True})

    pedido = db.session.get(Pedido, sample_pedido.id)
    assert pedido.cerrado is True

def test_editar_detalles(app_context, sample_pedido, sample_product):
    editar(sample_pedido.id, {
        "detalles": [{"producto_id": sample_product.id, "cantidad": 3}]
    })

    pedido = db.session.get(Pedido, sample_pedido.id)
    assert pedido.total == sample_product.precio * 3
    assert pedido.detalles[0].cantidad == 3

def test_editar_pedido_cerrado_no_permitido(app_context, sample_pedido, sample_product):
    sample_pedido.cerrado = True
    db.session.commit()

    with pytest.raises(ValueError, match="No se puede modificar un pedido cerrado"):
        editar(sample_pedido.id, {"detalles": [{"producto_id": sample_product.id, "cantidad": 5}]})

def test_editar_pedido_no_encontrado(app_context):
    with pytest.raises(ValueError, match="Pedido no encontrado"):
        editar(999, {"cerrado": True})

# ------------------------
# Tests eliminar()
# ------------------------

def test_eliminar_ok(app_context, sample_pedido):
    eliminar(sample_pedido.id)

    pedido = db.session.get(Pedido, sample_pedido.id)
    assert pedido is None

def test_eliminar_no_existe(app_context):
    with pytest.raises(ValueError, match="Pedido no encontrado"):
        eliminar(999)