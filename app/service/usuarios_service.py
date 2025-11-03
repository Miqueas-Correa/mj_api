from pydantic import ValidationError
from model.dto.UsuariosDTO import UsuarioSalidaDTO, UsuarioEntradaDTO, UsuarioUpdateDTO
from model.usuarios_model import Usuario, db
from werkzeug.security import generate_password_hash, check_password_hash

# PARA EL METODO GET
def listar(L_activos):
    try:
        if L_activos is not None:
            if L_activos.lower() == 'true':
                usuarios = Usuario.query.filter_by(activo=True).all()
            elif L_activos.lower() == 'false':
                usuarios = Usuario.query.filter_by(activo=False).all()
            else:
                raise ValueError("Error en el parámetro 'activos' debe ser 'true' o 'false'")
        else:
            usuarios = Usuario.query.all()

        if not usuarios:
            raise ValueError("No se encontraron usuarios")

        return [UsuarioSalidaDTO.from_model(u).__dict__ for u in usuarios]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar usuarios: " + str(e))

# buscar usuario por id o por nombre
def obtener(by_id, valor):
    try:
        if by_id:
            usuario = Usuario.query.get(valor)
            if not usuario: raise ValueError("Usuario no encontrado")
        else:
            usuario = Usuario.query.filter_by(nombre=valor).all()
            if not usuario: raise ValueError("Usuario no encontrado")
        return UsuarioSalidaDTO.from_model(usuario).__dict__
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar usuarios: " + str(e))

# PARA EL METODO POST
def crear(request):
    try:
        dto = UsuarioEntradaDTO(**request)
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
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al crear usuario: " + str(e))

# PARA EL METODO PUT
def editar(id, request, by_id):
    try:
        # busco por id o por nombre
        usuario = Usuario.query.get(id) if by_id else Usuario.query.filter_by(nombre=id).first()
        if not usuario: raise ValueError("Usuario no encontrado")

        dto = UsuarioUpdateDTO(**request)
        if not any([dto.nombre, dto.email, dto.telefono, dto.contrasenia]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False
        # Actualizar los campos del usuario
        if dto.nombre is not None:
            # Verificar si el nuevo nombre de usuario ya está en uso por otro usuario
            if usuario.nombre != dto.nombre and Usuario.query.filter_by(nombre=dto.nombre).first():
                raise ValueError("El nombre de usuario ya está registrado")
            usuario.nombre = dto.nombre
            modificado = True

        if dto.email is not None:
            # Verifico si el nuevo email ya está en uso por otro usuario
            if usuario.email != dto.email and Usuario.query.filter_by(email=dto.email).first():
                raise ValueError("El email ya está registrado")
            usuario.email = dto.email
            modificado = True

        if dto.telefono is not None:
            # Verifico si el nuevo telefono ya está en uso por otro usuario
            if usuario.telefono != dto.telefono and Usuario.query.filter_by(telefono=dto.telefono).first():
                raise ValueError("El teléfono ya está registrado")
            usuario.telefono = dto.telefono
            modificado = True

        if dto.contrasenia is not None:
            usuario.contrasenia = generate_password_hash(dto.contrasenia)
            modificado = True

        if not modificado:
            raise ValueError("No se pudo modificar al usuario")
        # Guardar los cambios en la base de datos
        db.session.commit()
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al modificar el usuario: " + str(e))

# PARA EL METODO POST DE COMPROBAR CONTRASEÑA, el metodo no funciona si la contrasenia
# no esta hasheada
def check_password(nombre_id, contrasenia, by_id):
    try:
        # busco el usuario por id o por nombre
        usuario = Usuario.query.get(nombre_id) if by_id else Usuario.query.filter_by(nombre=nombre_id).first()
        if not usuario or usuario.activo == False:
            raise ValueError("Usuario no encontrado")
        if not check_password_hash(usuario.contrasenia, contrasenia):
            raise ValueError("Contraseña incorrecta")
        return True
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al chekear la contraseña: " + str(e))

# PARA EL METODO DELETE
def eliminar(valor, by_id):
    try:
        # busco el usuario por id o por nombre
        usuario = Usuario.query.get(valor) if by_id else Usuario.query.filter_by(nombre=valor).first()
        if not usuario or usuario.activo == False: raise ValueError("Usuario no encontrado")
        usuario.activo = False
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al eliminar usuario: " + str(e))