from pydantic import ValidationError
from app.model.dto.PedidosDTO import PedidoUpdateDTO
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.model.productos_model import Producto
from app.model import db
from app.service.usuarios_service import obtener_U

"""
Módulo de servicio para la gestión de pedidos.
Funciones:
----------
- listar(L_cerrado):
    Lista todos los pedidos o los filtra según el estado de cerrado.
    Parámetros:
        L_cerrado (str | None): Filtra los pedidos por su estado de cerrado ('true' o 'false').
    Retorna:
        Lista de diccionarios con la información de los pedidos y sus detalles.
    Excepciones:
        ValueError: Si hay un error en los parámetros o no se encuentran pedidos.
- obtener(by, valor, L_cerrado):
    Obtiene pedidos filtrados por ID de usuario, ID de pedido o producto en los detalles.
    Parámetros:
        by (int): 0 para usuario, 1 para pedido, 2 para producto.
        valor (str/int): Valor a buscar según el filtro.
        L_cerrado (str | None): Filtra por estado de cerrado ('true' o 'false').
    Retorna:
        Lista de diccionarios con la información de los pedidos y sus detalles.
    Excepciones:
        ValueError: Si hay un error en los parámetros o no se encuentran pedidos.
- crear(data):
    Crea un nuevo pedido con los productos especificados.
    Parámetros:
        data (dict): Diccionario con 'id_usuario' y lista de productos (cada uno con 'producto_id' y 'cantidad').
    Excepciones:
        ValueError: Si hay un error al crear el pedido o algún producto no existe.
- editar(pedido_id, request):
    Edita un pedido existente, permitiendo modificar usuario, estado de cerrado y detalles.
    Parámetros:
        pedido_id (int): ID del pedido a modificar.
        request (dict): Diccionario con los campos a actualizar ('id_usuario', 'cerrado', 'detalles').
    Excepciones:
        ValueError: Si hay errores de validación, el pedido no existe o los datos son inválidos.
- eliminar(pedido_id):
    Elimina un pedido existente por su ID.
    Parámetros:
        pedido_id (int): ID del pedido a eliminar.
    Excepciones:
        ValueError: Si el pedido no existe o ocurre un error al eliminar.
"""

# GET - Listar todos o filtrados
def listar(L_cerrado):
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
def obtener(by, valor, L_cerrado):
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

# POST - Crear nuevo pedido
def crear(data):
    try:
        id_usuario = data["id_usuario"]
        productos_data = data["productos"]

        pedido = Pedido(id_usuario=id_usuario, total=0)
        total = 0

        for item in productos_data:
            producto = db.session.get(Producto, item["producto_id"])
            if not producto:
                raise ValueError(f"Producto {item['producto_id']} no encontrado")

            subtotal = producto.precio * item["cantidad"]
            total += subtotal

            detalle = PedidoDetalle(
                producto_id=producto.id,
                cantidad=item["cantidad"]
            )
            pedido.detalles.append(detalle)

        pedido.total = total
        db.session.add(pedido)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al crear pedido: " + str(e))

# PUT - Editar pedido existente
def editar(pedido_id, request):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: raise ValueError("Pedido no encontrado")

        campos_validos = {"id_usuario", "cerrado", "detalles"}
        for clave in request.keys():
            if clave not in campos_validos: raise ValueError(f"El atributo '{clave}' no existe en Pedido.")

        dto = PedidoUpdateDTO(**request)
        if not any([dto.id_usuario, dto.cerrado, dto.detalles]): raise ValueError("No se proporcionaron datos para actualizar")
        modificado = False

        if dto.id_usuario is not None:
            if obtener_U(True, dto.id_usuario) is None: raise ValueError(f"Usuario {dto.id_usuario} no encontrado")
            pedido.id_usuario = dto.id_usuario
            modificado = True

        if dto.cerrado is not None:
            pedido.cerrado = dto.cerrado
            modificado = True

        nuevos_detalles = []
        total = 0

        if dto.detalles is not None:
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

        if not modificado: raise ValueError("No se proporcionaron datos válidos para actualizar")

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
def eliminar(pedido_id):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: raise ValueError("Pedido no encontrado")

        db.session.delete(pedido)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al eliminar el pedido: " + str(e))