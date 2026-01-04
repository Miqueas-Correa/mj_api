from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import ValidationError
from app.model.token_blacklist import TokenBlacklist
from app.model.dto.UsuariosDTO import UsuarioEntradaDTO, UsuarioSalidaDTO
from app.model.usuarios_model import Usuario
from app.extensions import db

"""
Módulo de servicios para la gestión de usuarios en la aplicación.
Funciones:
----------
listar(L_activos):
    Lista los usuarios según su estado de actividad (activos/inactivos/todos).
    Parámetros:
        L_activos (str o None): 'true', 'false' o None para filtrar usuarios activos, inactivos o todos.
    Retorna:
        Lista de diccionarios con los datos de los usuarios.
    Excepciones:
        ValueError: Si el parámetro es inválido o no se encuentran usuarios.
obtener(id):
    Obtiene un usuario por su ID.
    Parámetros:
        id (int): ID del usuario.
    Retorna:
        Diccionario con los datos del usuario.
    Excepciones:
        ValueError: Si el usuario no existe.
crear(request):
    Crea un nuevo usuario a partir de los datos proporcionados.
    Parámetros:
        request (dict): Datos del usuario a crear.
    Excepciones:
        ValueError: Si hay errores de validación o datos duplicados.
editar(id, request, by_id):
    Edita los datos de un usuario existente.
    Parámetros:
        id (int o str): ID o nombre del usuario.
        request (dict): Datos a actualizar.
        by_id (bool): True si se busca por ID, False si por nombre.
    Excepciones:
        ValueError: Si hay errores de validación, datos duplicados o usuario no encontrado.
check_password(email, contrasenia):
    Verifica las credenciales de un usuario y genera tokens JWT si son correctas.
    Parámetros:
        email (str): Email del usuario.
        contrasenia (str): Contraseña del usuario.
    Retorna:
        Diccionario con tokens y datos del usuario.
    Excepciones:
        ValueError: Si las credenciales son incorrectas o el usuario está inactivo.
eliminar(valor, by_id):
    Marca un usuario como inactivo (eliminación lógica).
    Parámetros:
        valor (int o str): ID o nombre del usuario.
        by_id (bool): True si se busca por ID, False si por nombre.
    Retorna:
        Diccionario con mensaje de éxito.
    Excepciones:
        ValueError: Si el usuario no existe o ya está inactivo.
logout_token(jti):
    Revoca un token JWT añadiéndolo a la lista negra.
    Parámetros:
        jti (str): Identificador único del token JWT.
"""


# buscar usuario por id o por nombre
def obtener(id):
    try:
        usuario = db.session.get(Usuario, id)
        if not usuario: raise ValueError("Usuario no encontrado")
        return UsuarioSalidaDTO.from_model(usuario).__dict__
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar usuarios: " + str(e))

def check_password(email, contrasenia):
    try:
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.activo:
            raise ValueError("Usuario no encontrado o inactivo")

        if not usuario.check_password(contrasenia):
            raise ValueError("Contraseña incorrecta")

        access_token = create_access_token(
            identity=str(usuario.id),
            additional_claims={"rol": usuario.rol}
        )
        refresh_token = create_refresh_token(
            identity=str(usuario.id),
            additional_claims={"rol": usuario.rol}
        )

        return {
            "token": access_token,
            "refresh": refresh_token
        }

    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError(f"Error al comprobar la contraseña: {str(e)}")

def logout_token(jti: str):
    if TokenBlacklist.query.filter_by(jti=jti).first():
        return  # ya revocado

    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()

# crear usuario
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
