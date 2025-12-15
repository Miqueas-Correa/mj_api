from app.model.token_blacklist import TokenBlacklist
"""
Este módulo define los callbacks para la gestión de JWT, específicamente para verificar si un token ha sido revocado.
Funciones:
    register_jwt_callbacks(jwt):
        Registra los callbacks necesarios para la validación de JWT.
        - check_if_revoked(jwt_header, jwt_payload): Callback que verifica si el token (identificado por su JTI) se encuentra en la lista negra (revocado).
"""


def register_jwt_callbacks(jwt):

    @jwt.token_in_blocklist_loader
    def check_if_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlacklist.query.filter_by(jti=jti).first() is not None