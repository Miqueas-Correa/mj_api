import pytest
from app.model.productos_model import db, Producto
from app.model.usuarios_model import Usuario
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.service.admin_service import (
    listar_productos, obtener_productos, crear_producto, editar_producto, eliminar_producto,
    listar_usuarios, obtener_usuario, editar_usuario, eliminar_usuario,
    listar_pedidos, obtener_pedido, editar_pedido, eliminar_pedido
)

# ------------------------
# TEST listar_productos()
# ------------------------

def test_listar_productos_todos(app_context, sample_product):
    res = listar_productos(None)
    assert len(res) >= 1
    assert any(p["nombre"] == "TestProducto" for p in res)

def test_listar_productos_mostrar_true(app_context, sample_product):
    res = listar_productos("true")
    assert all(p["mostrar"] is True for p in res)

def test_listar_productos_mostrar_false(app_context, sample_product):
    sample_product.mostrar = False
    db.session.commit()
    res = listar_productos("false")
    assert all(p["mostrar"] is False for p in res)

def test_listar_productos_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'mostrar'"):
        listar_productos("otro")

# ------------------------
# TEST obtener_productos()
# ------------------------

def test_obtener_productos_por_id(app_context, sample_product):
    res = obtener_productos(1, sample_product.id, None)
    assert res[0]["nombre"] == "TestProducto"

def test_obtener_productos_por_nombre(app_context, sample_product):
    res = obtener_productos(0, "Test", None)
    assert len(res) >= 1

def test_obtener_productos_por_categoria(app_context, sample_product):
    res = obtener_productos(2, "Categoria1", None)
    assert len(res) >= 1

def test_obtener_productos_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto 999 no fue encontrado"):
        obtener_productos(1, 999, None)

# ------------------------
# TEST crear_producto()
# ------------------------

def test_crear_producto_ok(app_context):
    data = {
        "nombre": "NuevoProductoAdmin",
        "precio": 999.99,
        "stock": 15,
        "categoria": "test_admin",
        "descripcion": "Test admin",
        "imagen_url": "/img/test.jpg",
        "mostrar": True,
        "destacado": False
    }
    
    crear_producto(data)
    p = Producto.query.filter_by(nombre="NuevoProductoAdmin").first()
    assert p is not None
    assert float(p.precio) == 999.99

def test_crear_producto_nombre_duplicado(app_context, sample_product):
    data = {
        "nombre": "TestProducto",
        "precio": 100,
        "stock": 10,
        "categoria": "test",
        "descripcion": "desc",
        "imagen_url": "url",
        "mostrar": True,
        "destacado": False
    }
    
    with pytest.raises(ValueError, match="Ya existe un producto con ese nombre"):
        crear_producto(data)

# ------------------------
# TEST editar_producto()
# ------------------------

def test_editar_producto_precio(app_context, sample_product):
    editar_producto(sample_product.id, {"precio": 1500.00})
    p = db.session.get(Producto, sample_product.id)
    assert float(p.precio) == 1500.00

def test_editar_producto_mostrar(app_context, sample_product):
    editar_producto(sample_product.id, {"mostrar": False})
    p = db.session.get(Producto, sample_product.id)
    assert p.mostrar is False

def test_editar_producto_destacado(app_context, sample_product):
    editar_producto(sample_product.id, {"destacado": True})
    p = db.session.get(Producto, sample_product.id)
    assert p.destacado is True

def test_editar_producto_no_encontrado(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        editar_producto(999, {"precio": 100})

# ------------------------
# TEST eliminar_producto()
# ------------------------

def test_eliminar_producto_ok(app_context, sample_product):
    res = eliminar_producto(sample_product.id)
    assert res["message"] == "Producto eliminado exitosamente"
    assert db.session.get(Producto, sample_product.id) is None

def test_eliminar_producto_no_existe(app_context):
    with pytest.raises(ValueError, match="Producto no encontrado"):
        eliminar_producto(999)

# ------------------------
# TEST listar_usuarios()
# ------------------------

def test_listar_usuarios_todos(app_context, sample_user):
    res = listar_usuarios(None)
    assert len(res) >= 1

def test_listar_usuarios_activos(app_context, sample_user):
    res = listar_usuarios("true")
    assert all(u["activo"] is True for u in res)

def test_listar_usuarios_inactivos(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()
    res = listar_usuarios("false")
    assert all(u["activo"] is False for u in res)

def test_listar_usuarios_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'activos'"):
        listar_usuarios("otro")

# ------------------------
# TEST obtener_usuario()
# ------------------------

def test_obtener_usuario_por_id(app_context, sample_user):
    res = obtener_usuario(sample_user.id)
    assert res["nombre"] == "mike"

def test_obtener_usuario_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        obtener_usuario(999)

# ------------------------
# TEST editar_usuario()
# ------------------------

def test_editar_usuario_rol(app_context, sample_user):
    editar_usuario(sample_user.id, {"rol": "admin"})
    u = db.session.get(Usuario, sample_user.id)
    assert u.rol == "admin"

def test_editar_usuario_activo(app_context, sample_user):
    editar_usuario(sample_user.id, {"activo": False})
    u = db.session.get(Usuario, sample_user.id)
    assert u.activo is False

def test_editar_usuario_email_duplicado(app_context, sample_user):
    otro = Usuario(
        nombre="otro",
        email="otro@test.com",
        telefono="+5491199999999"
    )
    otro.set_password("pass")
    db.session.add(otro)
    db.session.commit()

    with pytest.raises(ValueError, match="El email ya está registrado"):
        editar_usuario(sample_user.id, {"email": "otro@test.com"})

# ------------------------
# TEST eliminar_usuario()
# ------------------------

def test_eliminar_usuario_ok(app_context, sample_user):
    res = eliminar_usuario(sample_user.id, by_id=True)
    assert res["message"] == "Usuario eliminado exitosamente"
    u = db.session.get(Usuario, sample_user.id)
    assert u.activo is False

def test_eliminar_usuario_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        eliminar_usuario(999, by_id=True)

# ------------------------
# TEST listar_pedidos()
# ------------------------

def test_listar_pedidos_todos(app_context, sample_pedido):
    res = listar_pedidos(None)
    assert len(res) >= 1

def test_listar_pedidos_cerrados(app_context, sample_pedido):
    sample_pedido.cerrado = True
    db.session.commit()
    res = listar_pedidos("true")
    assert all(p["cerrado"] is True for p in res)

def test_listar_pedidos_abiertos(app_context, sample_pedido):
    res = listar_pedidos("false")
    assert all(p["cerrado"] is False for p in res)

def test_listar_pedidos_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'cerrado'"):
        listar_pedidos("otro")

# ------------------------
# TEST obtener_pedido()
# ------------------------

def test_obtener_pedido_por_id(app_context, sample_pedido):
    res = obtener_pedido(1, sample_pedido.id, None)
    assert res[0]["id"] == sample_pedido.id

def test_obtener_pedido_por_usuario(app_context, sample_user, sample_pedido):
    res = obtener_pedido(0, sample_user.id, None)
    assert len(res) >= 1

def test_obtener_pedido_por_producto(app_context, sample_product, sample_pedido):
    res = obtener_pedido(2, sample_product.id, None)
    assert len(res) >= 1

def test_obtener_pedido_no_existe(app_context):
    with pytest.raises(ValueError, match="Pedido 999 no encontrado"):
        obtener_pedido(1, 999, None)

# ------------------------
# TEST editar_pedido()
# ------------------------

def test_editar_pedido_cerrar(app_context, sample_pedido):
    editar_pedido(sample_pedido.id, {"cerrado": True})
    p = db.session.get(Pedido, sample_pedido.id)
    assert p.cerrado is True

def test_editar_pedido_reabrir(app_context, sample_pedido):
    sample_pedido.cerrado = True
    db.session.commit()
    
    editar_pedido(sample_pedido.id, {"cerrado": False})
    p = db.session.get(Pedido, sample_pedido.id)
    assert p.cerrado is False

def test_editar_pedido_detalles(app_context, sample_pedido, sample_product):
    nuevos_detalles = [{"producto_id": sample_product.id, "cantidad": 5}]
    editar_pedido(sample_pedido.id, {"detalles": nuevos_detalles})
    
    p = db.session.get(Pedido, sample_pedido.id)
    assert len(p.detalles) == 1
    assert p.detalles[0].cantidad == 5

def test_editar_pedido_no_encontrado(app_context):
    with pytest.raises(ValueError, match="Pedido no encontrado"):
        editar_pedido(999, {"cerrado": True})

def test_editar_pedido_producto_inexistente(app_context, sample_pedido):
    detalles = [{"producto_id": 999, "cantidad": 1}]
    with pytest.raises(ValueError, match="Producto 999 no encontrado"):
        editar_pedido(sample_pedido.id, {"detalles": detalles})

# ------------------------
# TEST eliminar_pedido()
# ------------------------

def test_eliminar_pedido_ok(app_context, sample_pedido):
    eliminar_pedido(sample_pedido.id)
    p = db.session.get(Pedido, sample_pedido.id)
    assert p is None

def test_eliminar_pedido_no_existe(app_context):
    with pytest.raises(ValueError, match="Pedido no encontrado"):
        eliminar_pedido(999)