from pydantic import ValidationError
from app.model.dto.PedidosDTO import PedidoUpdateDTO
from app.model.dto.ProductosDTO import ProductoEntradaDTO, ProductoSalidaDTO, ProductoUpdateDTO
from app.model.dto.UsuariosDTO import UsuarioSalidaDTO, UsuarioUpdateDTO
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.model.productos_model import Producto
from app.extensions import db
from app.model.usuarios_model import Usuario

"""
    PRODUCTOS
"""
# listar productos
def listar_productos(L_mostrar):
    try:
        if L_mostrar is not None:
            if L_mostrar.lower() == 'true':
                productos = Producto.query.filter_by(mostrar=True).all()
            elif L_mostrar.lower() == 'false':
                productos = Producto.query.filter_by(mostrar=False).all()
            else:
                raise ValueError("Error en el parámetro 'mostrar' debe ser 'true' o 'false'")
        else:
            productos = Producto.query.all()
        return [ProductoSalidaDTO.from_model(u).__dict__ for u in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos: " + str(e))

# buscar productos por id, por nombre o categoria
def obtener_productos(by, valor, L_mostrar):
    try:
        if by not in [0, 1, 2]: raise ValueError("Error en el parámetro 'by' debe ser 0, 1 o 2")

        if by == 1:
            producto = db.session.get(Producto, valor)
            if not producto: raise ValueError(f"Producto {valor} no fue encontrado")
            productos = [producto]

        elif by == 0:
            productos = Producto.query.filter(Producto.nombre.like(f"%{valor}%")).all()
            if not productos: raise ValueError(f"No se encontraron productos con nombre similar a '{valor}'")

        else:  # by == 2
            productos = Producto.query.filter_by(categoria=valor).all()
            if not productos: raise ValueError(f"No se encontraron productos en la categoría '{valor}'")

        if L_mostrar is not None:
            if L_mostrar.lower() not in ['true', 'false']: raise ValueError("Error en el parámetro 'mostrar', debe ser 'true' o 'false'")

            mostrar_activos = L_mostrar.lower() == 'true'
            productos = [p for p in productos if p.mostrar == mostrar_activos]

            if not productos: raise ValueError("No se encontraron productos que coincidan con el filtro 'mostrar'")

        return [ProductoSalidaDTO.from_model(p).__dict__ for p in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos: " + str(e))

# Lista todos los productos destacados
def featured(L_mostrar):
    try:
        query = Producto.query.filter_by(destacado=True)
        if L_mostrar is not None:
            if L_mostrar.lower() == 'true':
                query = query.filter_by(mostrar=True)
            elif L_mostrar.lower() == 'false':
                query = query.filter_by(mostrar=False)
            else:
                raise ValueError("Error en el parámetro 'mostrar', debe ser 'true' o 'false'")
        productos = query.all()
        return [ProductoSalidaDTO.from_model(p).__dict__ for p in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos destacados: " + str(e))

# crear producto
def crear_producto(request):
    try:
        dto = ProductoEntradaDTO(**request)
        if Producto.query.filter_by(nombre=dto.nombre).first():
            raise ValueError("Ya existe un producto con ese nombre")

        nuevo_producto = Producto(
            nombre=dto.nombre,
            precio=dto.precio,
            stock=dto.stock,
            categoria=dto.categoria,
            descripcion=dto.descripcion,
            imagen_url=dto.imagen_url,
            mostrar=dto.mostrar,
            destacado=dto.destacado,
        )

        db.session.add(nuevo_producto)
        db.session.commit()
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error inesperado al crear el producto: {str(e)}")

# editar producto
def editar_producto(valor, request):
    try:
        producto = db.session.get(Producto, valor)
        if not producto: raise ValueError("Producto no encontrado")

        campos_validos = {"nombre", "precio", "stock", "categoria", "descripcion", "imagen_url", "mostrar", "destacado"}
        for clave in request.keys():
            if clave not in campos_validos: raise ValueError(f"El atributo '{clave}' no existe en Producto.")

        dto = ProductoUpdateDTO(**request)
        if not any([dto.nombre, dto.precio, dto.stock, dto.categoria,
                    dto.descripcion, dto.imagen_url, dto.mostrar]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False

        if dto.nombre is not None:
            if producto.nombre != dto.nombre and Producto.query.filter_by(nombre=dto.nombre).first():
                raise ValueError("El nombre del producto ya está registrado")
            producto.nombre = dto.nombre
            modificado = True

        if dto.precio is not None:
            producto.precio = dto.precio
            modificado = True

        if dto.stock is not None:
            producto.stock = dto.stock
            modificado = True

        if dto.categoria is not None:
            producto.categoria = dto.categoria
            modificado = True

        if dto.descripcion is not None:
            producto.descripcion = dto.descripcion
            modificado = True

        if dto.imagen_url is not None:
            producto.imagen_url = dto.imagen_url
            modificado = True

        if dto.mostrar is not None:
            producto.mostrar = dto.mostrar
            modificado = True

        if dto.destacado is not None:
            producto.destacado = dto.destacado
            modificado = True

        if not modificado:
            raise ValueError("No se pudo modificar el producto")

        db.session.commit()
    except ValidationError as e:
        db.session.rollback()
        raise ValueError("Error de validación: " + str(e))
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al modificar el producto: " + str(e))

# eliminar producto
def eliminar_producto(valor):
    try:
        producto = db.session.get(Producto, valor)
        if not producto: raise ValueError("Producto no encontrado")
        db.session.delete(producto)
        db.session.commit()
        return {"message": "Producto eliminado exitosamente"}
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al eliminar el producto: " + str(e))

"""
    USUARIOS
"""
# PARA EL METODO GET
def listar_usuarios(L_activos):
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

# buscar usuario por id
def obtener_usuario(id):
    try:
        usuario = db.session.get(Usuario, id)
        if not usuario: raise ValueError("Usuario no encontrado")
        return UsuarioSalidaDTO.from_model(usuario).__dict__
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar usuarios: " + str(e))

# editar usuario
def editar_usuario(user_id, request, es_admin=False):
    try:
        usuario = db.session.get(Usuario, user_id)
        if not usuario: 
            raise ValueError("Usuario no encontrado")

        campos_validos = {"nombre", "email", "telefono", "contrasenia"}

        if es_admin:
            campos_validos.add("rol")
            campos_validos.add("activo")

        for clave in request.keys():
            if clave not in campos_validos: 
                raise ValueError(f"No tienes permiso para modificar '{clave}'")

        dto = UsuarioUpdateDTO(**request)
        if not any([dto.nombre, dto.email, dto.telefono, dto.contrasenia, dto.rol if es_admin else None]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False

        if dto.nombre is not None:
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

        if es_admin and dto.rol is not None:
            if dto.rol not in ["cliente", "admin"]:
                raise ValueError("El rol debe ser 'cliente' o 'admin'")
            usuario.rol = dto.rol
            modificado = True

        if es_admin and "activo" in request:
            usuario.activo = request["activo"]
            modificado = True

        if not modificado: raise ValueError("No se modificó ningún campo")

        db.session.commit()

    except ValidationError as e:
        db.session.rollback()
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        db.session.rollback()
        raise ValueError(str(e))
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al modificar el usuario: " + str(e))

# eliminar usuario, se le da de baja (activo = False)
def eliminar_usuario(valor, by_id):
    try:
        usuario = db.session.get(Usuario, valor) if by_id else Usuario.query.filter_by(nombre=valor).first()
        if not usuario or usuario.activo == False: raise ValueError("Usuario no encontrado")
        usuario.activo = False
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al eliminar usuario: " + str(e))

"""
    PEDIDOS
"""
# GET - Listar todos o filtrados
def listar_pedidos(L_cerrado):
    try:
        if L_cerrado is not None:
            if L_cerrado.lower() == 'true':
                pedidos = Pedido.query.filter_by(cerrado=True).all()
            elif L_cerrado.lower() == 'false':
                pedidos = Pedido.query.filter_by(cerrado=False).all()
            else:
                raise ValueError("Error en el parámetro 'cerrado': debe ser 'true' o 'false'")
        else:
            pedidos = Pedido.query.all()

        if not pedidos: raise ValueError("No se encontraron pedidos")

        return [
            {
                "id": p.id,
                "id_usuario": p.id_usuario,
                "total": p.total,
                "fecha": p.fecha,
                "cerrado": p.cerrado,
                "detalles": [
                    {
                        "producto_id": d.producto_id,
                        "cantidad": d.cantidad,
                        "subtotal": d.cantidad * d.productos.precio
                    }
                    for d in p.detalles
                ]
            }
            for p in pedidos
        ]
    except Exception as e:
        raise ValueError("Error al listar pedidos: " + str(e))

# GET - Buscar por id, usuario o producto
def obtener_pedido(by, valor, L_cerrado):
    try:
        if by not in [0, 1, 2]: raise ValueError("Error en el parámetro 'by': debe ser 0, 1 o 2")

        if by == 1:  # por ID de pedido
            pedido = db.session.get(Pedido, valor)
            if not pedido: raise ValueError(f"Pedido {valor} no encontrado")
            pedidos = [pedido]

        elif by == 0:  # por ID de usuario
            pedidos = Pedido.query.filter(Pedido.id_usuario.like(f"%{valor}%")).all()
            if not pedidos: raise ValueError(f"No se encontraron pedidos del usuario '{valor}'")

        else:  # por producto (en detalles)
            pedidos = Pedido.query.join(PedidoDetalle).filter(PedidoDetalle.producto_id == valor).all()
            if not pedidos: raise ValueError(f"No se encontraron pedidos con el producto '{valor}'")

        # Filtrar por cerrado
        if L_cerrado is not None:
            if L_cerrado.lower() not in ['true', 'false']: raise ValueError("Error en el parámetro 'cerrado': debe ser 'true' o 'false'")

            cerrado_bool = L_cerrado.lower() == 'true'
            pedidos = [p for p in pedidos if p.cerrado == cerrado_bool]

            if not pedidos: raise ValueError("No se encontraron pedidos con el filtro 'cerrado'")

        if not pedidos: raise ValueError("No se encontraron pedidos")

        return [
            {
                "id": p.id,
                "id_usuario": p.id_usuario,
                "total": p.total,
                "fecha": p.fecha,
                "cerrado": p.cerrado,
                "detalles": [
                    {
                        "producto_id": d.producto_id,
                        "cantidad": d.cantidad,
                        "subtotal": d.cantidad * d.productos.precio
                    }
                    for d in p.detalles
                ]
            }
            for p in pedidos
        ]
    except Exception as e:
        raise ValueError("Error al obtener pedidos: " + str(e))

# PUT - Editar pedido existente
def editar_pedido(pedido_id, request):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: 
            raise ValueError("Pedido no encontrado")

        campos_validos = {"id_usuario", "cerrado", "detalles"}
        for clave in request.keys():
            if clave not in campos_validos: 
                raise ValueError(f"El atributo '{clave}' no existe en Pedido.")

        dto = PedidoUpdateDTO(**request)
        if not any([dto.id_usuario, dto.cerrado is not None, dto.detalles]):
            raise ValueError("No se proporcionaron datos para actualizar")
        
        modificado = False

        if dto.id_usuario is not None:
            usuario = db.session.get(Usuario, dto.id_usuario)
            if not usuario:
                raise ValueError(f"Usuario {dto.id_usuario} no encontrado")
            pedido.id_usuario = dto.id_usuario
            modificado = True

        # ✅ CORRECCIÓN: Permitir actualizar cerrado explícitamente
        if dto.cerrado is not None:
            pedido.cerrado = dto.cerrado
            modificado = True

        # Actualizar detalles si se proporcionan
        if dto.detalles is not None:
            nuevos_detalles = []
            total = 0

            for item in dto.detalles:
                producto = db.session.get(Producto, item.producto_id)
                if not producto:
                    raise ValueError(f"Producto {item.producto_id} no encontrado")

                subtotal = producto.precio * item.cantidad
                total += subtotal

                detalle = PedidoDetalle(
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                )
                nuevos_detalles.append(detalle)

            pedido.detalles.clear()
            pedido.detalles.extend(nuevos_detalles)
            pedido.total = total
            modificado = True

        if not modificado: 
            raise ValueError("No se proporcionaron datos válidos para actualizar")

        db.session.commit()
    except ValidationError as e:
        db.session.rollback()
        raise ValueError("Error de validación: " + str(e))
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al modificar el pedido: " + str(e))

# DELETE - Eliminar pedido
def eliminar_pedido(pedido_id):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: raise ValueError("Pedido no encontrado")

        db.session.delete(pedido)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al eliminar el pedido: " + str(e))