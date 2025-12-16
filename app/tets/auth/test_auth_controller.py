from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app.extensions import db
from app.model.token_blacklist import TokenBlacklist
from app.service.usuarios_service import logout_token

def test_login_ok(client, sample_user, monkeypatch):
    def mock_check_password(email, contrasenia):
        return {
            "token": "fake-access",
            "usuario": {
                "id": sample_user.id,
                "nombre": sample_user.nombre,
                "email": sample_user.email
            }
        }

    monkeypatch.setattr(
        "app.controller.auth_controller.check_password",
        mock_check_password
    )

    response = client.post(
        "/auth/login",
        json={"email": sample_user.email, "contrasenia": "1234"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["token"] == "fake-access"
    assert data["usuario"]["email"] == sample_user.email

def test_login_missing_fields(client):
    response = client.post("/auth/login", json={"email": "x@test.com"})
    assert response.status_code == 400

def test_login_invalid_credentials(client, monkeypatch):
    def mock_fail(email, contrasenia):
        raise ValueError("Contraseña incorrecta")

    monkeypatch.setattr(
        "app.controller.auth_controller.check_password",
        mock_fail
    )

    response = client.post(
        "/auth/login",
        json={"email": "x@test.com", "contrasenia": "bad"}
    )

    assert response.status_code == 400

def test_register_ok(client, monkeypatch):
    def mock_crear(data):
        return None

    monkeypatch.setattr(
        "app.controller.auth_controller.crear",
        mock_crear
    )

    response = client.post(
        "/auth/register",
        json={
            "nombre": "test",
            "email": "test@test.com",
            "telefono": "1123456789",
            "contrasenia": "123456"
        }
    )

    assert response.status_code == 201

def test_register_not_json(client):
    response = client.post("/auth/register", data="no-json")
    assert response.status_code == 400

def test_logout_ok(client, app):
    with app.app_context():
        token = create_access_token(
            identity=str(1),
            additional_claims={"rol": "cliente"}
        )

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.get_json()["message"].lower().startswith("logout")

def test_refresh_ok(client, app):
    with app.app_context():
        with app.app_context():
            refresh_token = create_refresh_token(
                identity=str(1),
                additional_claims={"rol": "cliente"}
            )

    response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data
    assert "refresh" in data

def test_logout_with_revoked_token(client, app):
    with app.app_context():
        token = create_access_token(
            identity=str(1),
            additional_claims={"rol": "cliente"}
        )

        # revocamos el token ANTES de usarlo
        jti = decode_token(token)["jti"]
        logout_token(jti)

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401