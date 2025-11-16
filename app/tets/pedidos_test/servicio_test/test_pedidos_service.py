import pytest
from app.model.pedidos_model import Pedido, db
from app.service.pedidos_service import listar, crear, editar, eliminar, obtener

"""
Este módulo contiene pruebas unitarias para el servicio de pedidos de la aplicación.
Funciones testeadas:
- listar(): Prueba la obtención de pedidos según diferentes parámetros, incluyendo casos de éxito y error.
- obtener(): Prueba la obtención de pedidos por ID, usuario, producto y manejo de errores por parámetros inválidos o inexistentes.
- crear(): Prueba la creación de pedidos, incluyendo el cálculo del total y manejo de productos inválidos.
- editar(): Prueba la edición de pedidos, tanto el cierre como la modificación de detalles, y el manejo de pedidos inexistentes.
- eliminar(): Prueba la eliminación de pedidos y el manejo de intentos de eliminar pedidos inexistentes.
Fixtures utilizados:
- app_context: Contexto de aplicación para las pruebas.
- sample_pedido: Pedido de ejemplo para pruebas.
- sample_user: Usuario de ejemplo para pruebas.
- sample_product: Producto de ejemplo para pruebas.
Las pruebas verifican tanto el comportamiento esperado como el manejo adecuado de errores mediante excepciones.
"""

# Tests listar()
def test_listar_todos(app_context, sample_pedido):
    res = listar(None)
    assert len(res) == 1
    assert res[0]["id_usuario"] == sample_pedido.id_usuario

def test_listar_cerrado_true_false(app_context, sample_pedido):
    sample_pedido.cerrado = True
    db.session.commit()

    res_true = listar("true")
    assert len(res_true) == 1
    assert res_true[0]["cerrado"] is True
    with pytest.raises(ValueError, match="No se encontraron pedidos"):
        listar("false")

def test_listar_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'cerrado'"):
        listar("otro")

# Tests obtener()
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

# Tests crear()
def test_crear_ok(app_context, sample_user, sample_product):
    data = {
        "id_usuario": sample_user.id,
        "productos": [{"producto_id": sample_product.id, "cantidad": 2}]
    }
    crear(data)
    pedido = Pedido.query.filter_by(id_usuario=sample_user.id).order_by(Pedido.id.desc()).first()
    assert pedido.total == sample_product.precio * 2
    assert len(pedido.detalles) == 1

def test_crear_producto_invalido(app_context, sample_user):
    data = {
        "id_usuario": sample_user.id,
        "productos": [{"producto_id": 999, "cantidad": 1}]
    }
    with pytest.raises(ValueError, match="Producto 999 no encontrado"):
        crear(data)

# Tests editar()
def test_editar_cerrado(app_context, sample_pedido):
    editar(sample_pedido.id, {"cerrado": True})
    pedido = db.session.get(Pedido, sample_pedido.id)
    assert pedido.cerrado is True

def test_editar_detalles(app_context, sample_pedido, sample_product):
    editar(sample_pedido.id, {"detalles": [{"producto_id": sample_product.id, "cantidad": 3}]})
    pedido = db.session.get(Pedido, sample_pedido.id)
    assert pedido.total == sample_product.precio * 3
    assert pedido.detalles[0].cantidad == 3

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