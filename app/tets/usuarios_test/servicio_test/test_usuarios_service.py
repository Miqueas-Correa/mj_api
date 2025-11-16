import pytest
from app.model.usuarios_model import db, Usuario
from app.service.usuarios_service import listar, obtener_U, crear, editar, check_password, eliminar
"""
Pruebas unitarias para el servicio de usuarios.
Este módulo contiene pruebas para las funciones del servicio de usuarios, incluyendo:
- listar: Listado de usuarios activos/inactivos y manejo de parámetros inválidos o sin resultados.
- obtener_U: Obtención de usuario por ID o nombre, y manejo de usuario inexistente.
- crear: Creación de usuarios, validación de unicidad de email, teléfono y nombre.
- editar: Edición de atributos de usuario, validación de unicidad, atributos inexistentes, sin cambios y usuario inexistente.
- check_password: Verificación de contraseña correcta, incorrecta y usuario inactivo.
- eliminar: Eliminación lógica de usuario, manejo de usuario inexistente o ya inactivo.
Fixtures requeridas:
- app_context: Contexto de aplicación para pruebas.
- sample_user: Usuario de ejemplo para pruebas.
Las pruebas verifican tanto los casos exitosos como los errores esperados mediante el uso de pytest.raises.
"""

# TESTS PARA listar()
def test_listar_activos(app_context, sample_user):
    resultado = listar("true")
    assert len(resultado) == 1
    assert resultado[0]["activo"] is True

def test_listar_inactivos(app_context, sample_user):
    # marcar inactivo
    sample_user.activo = False
    db.session.commit()

    resultado = listar("false")
    assert len(resultado) == 1
    assert resultado[0]["activo"] is False

def test_listar_parametro_invalido(app_context):
    with pytest.raises(ValueError, match="Error en el parámetro 'activos'"):
        listar("otro")

def test_listar_sin_resultados(app_context):
    # eliminar todos los usuarios para probar sin resultados
    Usuario.query.delete()
    db.session.commit()
    with pytest.raises(ValueError, match="No se encontraron usuarios"):
        listar("true")

# TEST obtener_U()
def test_obtener_por_id(app_context, sample_user):
    res = obtener_U(True, sample_user.id)
    assert res["nombre"] == "mike"

def test_obtener_por_nombre(app_context, sample_user):
    res = obtener_U(False, "mike")
    assert res["email"] == "mike@test.com"

def test_obtener_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        obtener_U(True, 999)

# TEST crear()
def test_crear_ok(app_context):
    data = {
        "nombre": "juan",
        "email": "juan@test.com",
        "telefono": "1123456789",
        "contrasenia": "abcdef"
    }
    crear(data)
    u = Usuario.query.filter_by(email="juan@test.com").first()
    assert u is not None
    assert u.nombre == "juan"

def test_crear_email_repetido(app_context, sample_user):
    data = {
        "nombre": "otro",
        "email": "mike@test.com",
        "telefono": "1123456789",
        "contrasenia": "abcdef"
    }
    with pytest.raises(ValueError, match="El email ya está registrado"):
        crear(data)

def test_crear_telefono_repetido(app_context, sample_user):
    data = {
        "nombre": "otro",
        "email": "otro@test.com",
        "telefono": sample_user.telefono,
        "contrasenia": "abcdef"
    }
    with pytest.raises(ValueError, match="El teléfono ya está registrado"):
        crear(data)

def test_crear_nombre_repetido(app_context, sample_user):
    data = {
        "nombre": "mike",
        "email": "xd@test.com",
        "telefono": "1123456790",
        "contrasenia": "abcdef"
    }
    with pytest.raises(ValueError, match="El nombre de usuario ya está registrado"):
        crear(data)

# TEST editar()
def test_editar_nombre_correctamente(app_context, sample_user):
    editar(sample_user.id, {"nombre": "nuevo"}, True)
    u = db.session.get(Usuario, sample_user.id)
    assert u.nombre == "nuevo"

def test_editar_email_repetido(app_context, sample_user):
    other = Usuario(
        nombre="otro",
        email="otro@test.com",
        telefono="888",
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
    with pytest.raises(ValueError, match="No se proporcionaron datos para actualizar"):
        editar(sample_user.id, {}, True)

def test_editar_no_existe(app_context):
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        editar(999, {"nombre": "a"}, True)

# TEST check_password()
def test_check_password_ok(app_context, sample_user):
    assert check_password("mike", "1234", False) is True

def test_check_password_incorrecta(app_context, sample_user):
    with pytest.raises(ValueError, match="Contraseña incorrecta"):
        check_password("mike", "0000", False)

def test_check_password_usuario_inactivo(app_context, sample_user):
    sample_user.activo = False
    db.session.commit()
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        check_password("mike", "1234", False)

# TEST eliminar()
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