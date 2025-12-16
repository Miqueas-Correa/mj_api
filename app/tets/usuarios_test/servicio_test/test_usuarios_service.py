import pytest
from app.model.usuarios_model import db, Usuario
from app.service.usuarios_service import listar, obtener, crear, editar, check_password, eliminar

# ------------------------
# TEST listar()
# ------------------------

def test_listar_activos(app_context, sample_user):
    resultado = listar("true")
    assert len(resultado) == 1
    assert resultado[0]["activo"] is True

def test_listar_inactivos(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()

    resultado = listar("false")
    assert len(resultado) == 1
    assert resultado[0]["activo"] is False

def test_listar_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'activos'"):
        listar("otro")

def test_listar_sin_resultados(app_context):
    Usuario.query.delete()
    db.session.commit()

    with pytest.raises(ValueError, match="No se encontraron usuarios"):
        listar("true")

# ------------------------
# TEST obtener()
# ------------------------

def test_obtener_por_id(app_context, sample_user):
    res = obtener(sample_user.id)
    assert res["nombre"] == "mike"

def test_obtener_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        obtener(999)

# ------------------------
# TEST crear()
# ------------------------

def test_crear_ok(app_context):
    data = {
        "nombre": "juan",
        "email": "juan@test.com",
        "telefono": "1123456789",
        "contrasenia": "abcdef",
        "acepta_uso_datos": True
    }

    crear(data)
    u = Usuario.query.filter_by(email="juan@test.com").first()
    assert u is not None
    assert u.nombre == "juan"

def test_crear_email_repetido(app_context, sample_user):
    data = {
        "nombre": "otro",
        "email": "mike@test.com",
        "telefono": "1123456799",
        "contrasenia": "abcdef",
        "acepta_uso_datos": True
    }

    with pytest.raises(ValueError, match="El email ya está registrado"):
        crear(data)

def test_crear_telefono_repetido(app_context, sample_user):
    data = {
        "nombre": "otro",
        "email": "otro@test.com",
        "telefono": sample_user.telefono,
        "contrasenia": "abcdef",
        "acepta_uso_datos": True
    }

    with pytest.raises(ValueError, match="El teléfono ya está registrado"):
        crear(data)

def test_crear_nombre_repetido(app_context, sample_user):
    data = {
        "nombre": "mike",
        "email": "xd@test.com",
        "telefono": "1123456790",
        "contrasenia": "abcdef",
        "acepta_uso_datos": True
    }

    with pytest.raises(ValueError, match="El nombre de usuario ya está registrado"):
        crear(data)

def test_crear_sin_aceptar_uso_datos(app_context):
    with pytest.raises(ValueError, match="Debes aceptar el uso de datos"):
        crear({
            "nombre": "juan",
            "email": "juan2@test.com",
            "telefono": "1123456798",
            "contrasenia": "abcdef"
        })

# ------------------------
# TEST editar()
# ------------------------

def test_editar_nombre_correctamente(app_context, sample_user):
    editar(sample_user.id, {"nombre": "nuevo"}, True)
    u = db.session.get(Usuario, sample_user.id)
    assert u.nombre == "nuevo"

def test_editar_email_repetido(app_context, sample_user):
    other = Usuario(
        nombre="otro",
        email="otro@test.com",
        telefono="+5491122222222",
        contrasenia="x"
    )
    db.session.add(other)
    db.session.commit()

    with pytest.raises(ValueError, match="El email ya está registrado"):
        editar(sample_user.id, {"email": "otro@test.com"}, True)

def test_editar_atributo_inexistente(app_context, sample_user):
    with pytest.raises(ValueError, match="no existe en Usuario"):
        editar(sample_user.id, {"xd": "valor"}, True)

def test_editar_sin_cambios(app_context, sample_user):
    with pytest.raises(ValueError, match="No se proporcionaron datos|No se pudo modificar"):
        editar(sample_user.id, {}, True)

def test_editar_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        editar(999, {"nombre": "a"}, True)

# ------------------------
# TEST check_password()
# ------------------------

def test_check_password_ok(app_context, sample_user):
    res = check_password("mike@test.com", "1234")
    assert "token" in res
    assert res["usuario"]["email"] == "mike@test.com"

def test_check_password_incorrecta(app_context, sample_user):
    with pytest.raises(ValueError, match="Contraseña incorrecta"):
        check_password("mike@test.com", "0000")

def test_check_password_usuario_inactivo(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()

    with pytest.raises(ValueError, match="Usuario no encontrado"):
        check_password("mike@test.com", "1234")

# ------------------------
# TEST eliminar()
# ------------------------

def test_eliminar_ok(app_context, sample_user):
    res = eliminar(sample_user.id, True)
    assert res["message"] == "Usuario eliminado exitosamente"

    u = db.session.get(Usuario, sample_user.id)
    assert u.activo is False

def test_eliminar_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        eliminar(999, True)

def test_eliminar_inactivo(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()

    with pytest.raises(ValueError, match="Usuario no encontrado"):
        eliminar(sample_user.id, True)