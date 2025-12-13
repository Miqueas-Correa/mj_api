from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import ValidationError
from app.model.dto.UsuariosDTO import UsuarioSalidaDTO, UsuarioEntradaDTO, UsuarioUpdateDTO
from app.model.usuarios_model import Usuario
from app.extensions import db

"""
Módulo de servicios para la gestión de usuarios.
Funciones:
----------
listar(L_activos):
    Lista los usuarios del sistema, filtrando por activos o inactivos si se especifica.
    Parámetros:
        L_activos (str | None): 'true' para activos, 'false' para inactivos, None para todos.
    Retorna:
        Lista de diccionarios con los datos de los usuarios.
    Excepciones:
        ValueError: Si el parámetro es inválido o no se encuentran usuarios.
obtener_U(by_id, valor):
    Obtiene un usuario por ID o por nombre.
    Parámetros:
        by_id (bool): True para buscar por ID, False para buscar por nombre.
        valor (int | str): ID o nombre del usuario.
    Retorna:
        Diccionario con los datos del usuario.
    Excepciones:
        ValueError: Si no se encuentra el usuario.
crear(request):
    Crea un nuevo usuario en el sistema.
    Parámetros:
        request (dict): Datos del usuario a crear.
    Excepciones:
        ValueError: Si hay errores de validación o datos duplicados.
editar(id, request, by_id):
    Edita los datos de un usuario existente.
    Parámetros:
        id (int | str): ID o nombre del usuario a editar.
        request (dict): Datos a actualizar.
        by_id (bool): True para buscar por ID, False para buscar por nombre.
    Excepciones:
        ValueError: Si hay errores de validación, datos duplicados o no se encuentra el usuario.
check_password(nombre_id, contrasenia, by_id):
    Verifica la contraseña de un usuario.
    Parámetros:
        nombre_id (int | str): ID o nombre del usuario.
        contrasenia (str): Contraseña a verificar.
        by_id (bool): True para buscar por ID, False para buscar por nombre.
    Retorna:
        True si la contraseña es correcta.
    Excepciones:
        ValueError: Si el usuario no existe, está inactivo o la contraseña es incorrecta.
eliminar(valor, by_id):
    Marca un usuario como inactivo (eliminación lógica).
    Parámetros:
        valor (int | str): ID o nombre del usuario.
        by_id (bool): True para buscar por ID, False para buscar por nombre.
    Retorna:
        dict: Mensaje de éxito.
    Excepciones:
        ValueError: Si el usuario no existe o está inactivo.
"""

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
def obtener_U(by_id, valor):
    try:
        if by_id:
            usuario = db.session.get(Usuario, valor)
            if not usuario: raise ValueError("Usuario no encontrado")
        else:
            usuario = Usuario.query.filter_by(nombre=valor).first()
            if not usuario: raise ValueError("Usuario no encontrado")
        return UsuarioSalidaDTO.from_model(usuario).__dict__
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar usuarios: " + str(e))

# PARA EL METODO POST
def crear(request):
    try:
        if not request.get("acepta_uso_datos", False):
            raise ValueError("Debes aceptar el uso de datos para continuar")
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
            telefono=dto.telefono
        )
        nuevo_usuario.set_password(dto.contrasenia)

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
        usuario = db.session.get(Usuario, id) if by_id else Usuario.query.filter_by(nombre=id).first()
        if not usuario: raise ValueError("Usuario no encontrado")

        campos_validos = {"nombre", "email", "telefono", "contrasenia", "rol"}
        for clave in request.keys():
            if clave not in campos_validos: 
                raise ValueError(f"El atributo '{clave}' no existe en Usuario.")

        dto = UsuarioUpdateDTO(**request)
        if not any([dto.nombre, dto.email, dto.telefono, dto.contrasenia, dto.rol]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False
        # Actualizar los campos del usuario
        if dto.nombre is not None:
            if usuario.nombre != dto.nombre and Usuario.query.filter_by(nombre=dto.nombre).first():
                raise ValueError("El nombre de usuario ya está registrado")
            usuario.nombre = dto.nombre
            modificado = True

        if dto.email is not None:
            if usuario.email != dto.email and Usuario.query.filter_by(email=dto.email).first():
                raise ValueError("El email ya está registrado")
            usuario.email = dto.email
            modificado = True

        if dto.telefono is not None:
            if usuario.telefono != dto.telefono and Usuario.query.filter_by(telefono=dto.telefono).first():
                raise ValueError("El teléfono ya está registrado")
            usuario.telefono = dto.telefono
            modificado = True

        if dto.contrasenia is not None:
            usuario.set_password(dto.contrasenia)
            modificado = True

        if dto.rol is not None:
            usuario.rol = dto.rol
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

def check_password(email, contrasenia):
    try:
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.activo:
            raise ValueError("Usuario no encontrado o inactivo")

        if not usuario.check_password(contrasenia):
            raise ValueError("Contraseña incorrecta")

        access_token = create_access_token(
            identity=usuario.id,
            additional_claims={"rol": usuario.rol}
        )
        refresh_token = create_refresh_token(identity=usuario.id)

        return {
            "token": access_token,
            "refresh": refresh_token,
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "rol": usuario.rol
            }
        }

    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError(f"Error al comprobar la contraseña: {str(e)}")

# PARA EL METODO DELETE
def eliminar(valor, by_id):
    try:
        usuario = db.session.get(Usuario, valor) if by_id else Usuario.query.filter_by(nombre=valor).first()
        if not usuario or usuario.activo == False: 
            raise ValueError("Usuario no encontrado")
        usuario.activo = False
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al eliminar usuario: " + str(e))