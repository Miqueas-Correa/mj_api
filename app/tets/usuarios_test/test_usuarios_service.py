import pytest
from app.model.usuarios_model import db, Usuario
from app.service.usuarios_service import obtener, crear, check_password

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
# TEST check_password()
# ------------------------

def test_check_password_ok(app_context, sample_user):
    res = check_password("mike@test.com", "1234")
    assert "token" in res
    assert "refresh" in res

def test_check_password_incorrecta(app_context, sample_user):
    with pytest.raises(ValueError, match="Contraseña incorrecta"):
        check_password("mike@test.com", "0000")

def test_check_password_usuario_inactivo(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()

    with pytest.raises(ValueError, match="Usuario no encontrado"):
        check_password("mike@test.com", "1234")