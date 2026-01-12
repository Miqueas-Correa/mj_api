from flask_jwt_extended import create_access_token, create_refresh_token
from pydantic import ValidationError
from app.model.token_blacklist import TokenBlacklist
from app.model.dto.Usuarios_dto import UsuarioEntradaDTO, UsuarioSalidaDTO
from app.model.usuarios_model import Usuario
from app.extensions import db
"""
Módulo de servicios para la gestión de usuarios.
Funciones:
- obtener(id): Busca y retorna un usuario por su ID. Lanza ValueError si no se encuentra.
- check_password(email, contrasenia): Verifica las credenciales del usuario y retorna tokens JWT si son correctas. Lanza ValueError en caso de error de validación, usuario inactivo/no encontrado o contraseña incorrecta.
- logout_token(jti): Revoca un token JWT añadiendo su JTI a la lista negra.
- crear(request): Crea un nuevo usuario a partir de los datos recibidos en el request. Valida unicidad de email, teléfono y nombre de usuario, y que se acepte el uso de datos. Lanza ValueError en caso de error de validación o si ya existen los datos.
Excepciones:
- ValueError: Se lanza en caso de errores de validación, datos duplicados o problemas al interactuar con la base de datos.
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