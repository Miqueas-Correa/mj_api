from app.model.dto.UsuarioDTO import UsuarioSalidaDTO
from model.usuarios_model import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from model.usuarios_model import db

# PARA EL METODO GET
def listar_usuarios_service(L_activos):
    if L_activos is not None:
        if L_activos.lower() == 'true':
            usuarios = Usuario.query.filter_by(activo=True).all()
        elif L_activos.lower() == 'false':
            usuarios = Usuario.query.filter_by(activo=False).all()
        else:
            raise ValueError("Error en el parámetro 'activos' debe ser 'true' o 'false'")
    else:
        usuarios = Usuario.query.all()
    return [UsuarioSalidaDTO.from_model(u).__dict__ for u in usuarios]

# buscar usuario por id o por nombre
def obtener_usuario(by_id, valor, L_activos):
    if by_id:
        usuario = Usuario.query.get(valor)
    else:
        usuario = Usuario.query.filter_by(nombre=valor).first()
    if L_activos is not None:
        if L_activos.lower() == 'true' and (not usuario or not usuario.activo):
            raise ValueError("Usuario no encontrado")
        elif L_activos.lower() == 'false' and (not usuario or usuario.activo):
            raise ValueError("Usuario no encontrado")
        elif L_activos.lower() not in ['true', 'false']:
            raise ValueError("Error en el parámetro 'activos' debe ser 'true' o 'false'")
    return UsuarioSalidaDTO.from_model(usuario).__dict__

# PARA EL METODO POST
def usuario_nuevo(dto):
    # email único
    if Usuario.query.filter_by(email=dto.email).first():
        raise ValueError("El email ya está registrado")
    # telefono unico
    if Usuario.query.filter_by(telefono=dto.telefono).first():
        raise ValueError("El teléfono ya está registrado")
    # nombre de usuario unico
    if Usuario.query.filter_by(nombre=dto.nombre).first():
        raise ValueError("El nombre de usuario ya está registrado")

    # Si pasa, creo el usuario
    nuevo_usuario = Usuario(
        nombre=dto.nombre,
        email=dto.email,
        telefono=dto.telefono,
        contrasenia=generate_password_hash(dto.contrasenia)#,
        # activo=dto.activo,
        # rol=dto.rol
    )

    db.session.add(nuevo_usuario) # prepara la insercion
    db.session.commit() # ejecuta la insercion en la base de datos

# PARA EL METODO PUT
def editar_usuario(id, dto):
    # Buscar el usuario por su nombre actual
    usuario = Usuario.query.get(id).first()
    if not usuario: return ValueError("Usuario no encontrado")

    # Actualizar los campos del usuario
    if dto.nombre is not None:
        # Verificar si el nuevo nombre de usuario ya está en uso por otro usuario
        if usuario.nombre != dto.nombre and Usuario.query.filter_by(nombre=dto.nombre).first():
            raise ValueError("El nombre de usuario ya está registrado")
        usuario.nombre = dto.nombre

    if dto.email is not None:
        # Verifico si el nuevo email ya está en uso por otro usuario
        if usuario.email != dto.email and Usuario.query.filter_by(email=dto.email).first():
            raise ValueError("El email ya está registrado")
        usuario.email = dto.email

    if dto.telefono is not None:
        # Verifico si el nuevo telefono ya está en uso por otro usuario
        if usuario.telefono != dto.telefono and Usuario.query.filter_by(telefono=dto.telefono).first():
            raise ValueError("El teléfono ya está registrado")
        usuario.telefono = dto.telefono

    if dto.contrasenia is not None:
        usuario.contrasenia = generate_password_hash(dto.contrasenia)

    # Guardar los cambios en la base de datos
    db.session.commit()

# PARA EL METODO POST DE COMPROBAR CONTRASEÑA, el metodo no funciona si la contrasenia
# no esta hasheada
def check_password(nombre_id, contrasenia, by_id):
    # busco el usuario por id o por nombre
    usuario = Usuario.query.get(nombre_id) if by_id else Usuario.query.filter_by(nombre=nombre_id).first()
    if not usuario or usuario.activo == False:
        raise ValueError("Usuario no encontrado")
    if not check_password_hash(usuario.contrasenia, contrasenia):
        raise ValueError("Contraseña incorrecta")
    return True

# PARA EL METODO DELETE
def eliminar_usuario_service(valor, by_id=True):
    # busco el usuario por id o por nombre
    usuario = Usuario.query.get(valor) if by_id else Usuario.query.filter_by(nombre=valor).first()
    if not usuario or usuario.activo == False: raise ValueError("Usuario no encontrado")
    usuario.activo = False
    db.session.commit()
    return {"message": "Usuario eliminado exitosamente"}