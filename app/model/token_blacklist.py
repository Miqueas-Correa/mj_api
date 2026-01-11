from datetime import datetime, timezone
from app.extensions import db

"""
Modelo para la tabla 'token_blacklist' que almacena los tokens JWT invalidados.
Atributos:
    id (int): Identificador único y clave primaria de la tabla.
    jti (str): Identificador único del token JWT (JWT ID), no puede repetirse ni ser nulo.
    created_at (datetime): Fecha y hora en que el token fue añadido a la lista negra, con zona horaria UTC.
"""

class TokenBlacklist(db.Model):
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)