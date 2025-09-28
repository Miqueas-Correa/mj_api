from model.usuarios_model import Usuario
from werkzeug.security import generate_password_hash

def usuario_nuevo(dto):
    # email único
    if Usuario.query.filter_by(email=dto.email).first():
        raise ValueError("El email ya está registrado")
    # telefono unico
    if Usuario.query.filter_by(telefono=dto.telefono).first():
        raise ValueError("El teléfono ya está registrado")

    # Si pasa, creo el usuario
    nuevo_usuario = Usuario(
        nombre=dto.nombre,
        email=dto.email,
        telefono=dto.telefono,
        contrasenia=generate_password_hash(dto.contrasenia)#,
        # activo=dto.activo,
        # rol=dto.rol
    )

    return nuevo_usuario