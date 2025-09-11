def getUsuario(nombre_apellido: str):
    for usuario in usuarios_db:
        if usuario.nombre_apellido == nombre_apellido:
            return usuario
    return None

# get all usuarios: retorna todos los usuarios de la base de datos
def getUsuarios():
    return usuarios_db

def getUsuarioId(id: int):
    for usuario in usuarios_db:
        if usuario.id == id:
            return usuario
    return None

def login(nombre_apellido: str, telefono: str, email: str, contraseña: str):
    for usuario in usuarios_db:
        if (usuario.nombre_apellido == nombre_apellido and
            usuario.telefono == telefono and
            usuario.email == email and
            usuario.contraseña == contraseña):
            return usuario
    return None

def deleteUsuario(id: int):
    global usuarios_db
    for i, usuario in enumerate(usuarios_db):
        if usuario.id == id:
            del usuarios_db[i]
            admin_ids.discard(id)
            return True
    return False

def asignarAdmin(id: int):
    usuario = getUsuarioId(id)
    if usuario:
        usuario.es_admin = True
        admin_ids.add(id)
        return True
    return False

def inicioSecion(email: str, contraseña: str):
    for usuario in usuarios_db:
        if usuario.email == email and usuario.contraseña == contraseña:
            return usuario
    return None