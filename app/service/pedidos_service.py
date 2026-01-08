from pydantic import ValidationError
from app.model.dto.PedidosDTO import PedidoUpdateDTO
from app.model.pedidos_model import Pedido, PedidoDetalle
from app.model.productos_model import Producto
from app.extensions import db
from app.service.usuarios_service import obtener

"""
Módulo de servicio para la gestión de pedidos con control de stock.
"""

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

# POST - Crear nuevo pedido con validación de stock
def crear(data):
    try:
        id_usuario = data["id_usuario"]
        productos_data = data["productos"]

        # Primero validar que todos los productos existan y tengan stock suficiente
        productos_validados = []
        for item in productos_data:
            producto = db.session.get(Producto, item["producto_id"])
            if not producto:
                raise ValueError(f"Producto {item['producto_id']} no encontrado")
            
            # Validar stock disponible
            if producto.stock < item["cantidad"]:
                raise ValueError(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {item['cantidad']}")
            
            productos_validados.append({
                "producto": producto,
                "cantidad": item["cantidad"]
            })

        # Si todo está bien, crear el pedido y descontar stock
        pedido = Pedido(id_usuario=id_usuario, total=0)
        total = 0

        for item in productos_validados:
            producto = item["producto"]
            cantidad = item["cantidad"]
            
            subtotal = producto.precio * cantidad
            total += subtotal

            # Descontar stock
            producto.stock -= cantidad
            
            # Ocultar producto si se agota el stock
            if producto.stock <= 0:
                producto.mostrar = False

            detalle = PedidoDetalle(
                producto_id=producto.id,
                cantidad=cantidad
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
        # si el pedido esta cerrado, no se puede modificar
        if pedido.cerrado: raise ValueError("No se puede modificar un pedido cerrado")
        campos_validos = {"id_usuario", "cerrado", "detalles"}
        for clave in request.keys():
            if clave not in campos_validos: raise ValueError(f"El atributo '{clave}' no existe en Pedido.")

        dto = PedidoUpdateDTO(**request)
        if not any([dto.id_usuario, dto.cerrado, dto.detalles]): raise ValueError("No se proporcionaron datos para actualizar")
        modificado = False

        if dto.id_usuario is not None:
            if obtener(0, dto.id_usuario) is None: raise ValueError(f"Usuario {dto.id_usuario} no encontrado")
            pedido.id_usuario = dto.id_usuario
            modificado = True

        if dto.cerrado is not None:
            pedido.cerrado = dto.cerrado
            modificado = True

        nuevos_detalles = []
        total = 0

        if dto.detalles is not None:
            # Primero devolver el stock de los productos actuales
            for detalle_actual in pedido.detalles:
                producto_actual = db.session.get(Producto, detalle_actual.producto_id)
                if producto_actual:
                    producto_actual.stock += detalle_actual.cantidad
                    # Mostrar el producto si vuelve a tener stock
                    if producto_actual.stock > 0:
                        producto_actual.mostrar = True
            
            # Validar nuevo stock antes de actualizar
            for item in dto.detalles:
                producto = db.session.get(Producto, item.producto_id)
                if not producto:
                    raise ValueError(f"Producto {item.producto_id} no encontrado")
                
                if producto.stock < item.cantidad:
                    raise ValueError(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {item.cantidad}")

            # Si todo está bien, actualizar
            for item in dto.detalles:
                producto = db.session.get(Producto, item.producto_id)
                
                subtotal = producto.precio * item.cantidad
                total += subtotal

                # Descontar el nuevo stock
                producto.stock -= item.cantidad
                
                # Ocultar producto si se agota
                if producto.stock <= 0:
                    producto.mostrar = False

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

# NUEVO - Cancelar pedido y devolver stock
def cancelar(pedido_id, id_usuario):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: 
            raise ValueError("Pedido no encontrado")
        
        # Validar que el pedido pertenece al usuario (comparar como string)
        if str(pedido.id_usuario) != str(id_usuario):
            raise ValueError(f"No tienes permiso para cancelar este pedido. Usuario del pedido: {pedido.id_usuario}, Usuario actual: {id_usuario}")
        
        # No se puede cancelar un pedido ya cerrado
        if pedido.cerrado: 
            raise ValueError("No se puede cancelar un pedido ya finalizado")
        
        # Devolver el stock de todos los productos
        for detalle in pedido.detalles:
            producto = db.session.get(Producto, detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                # Mostrar el producto si vuelve a tener stock
                if producto.stock > 0:
                    producto.mostrar = True
        
        # Eliminar el pedido
        db.session.delete(pedido)
        db.session.commit()
        
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al cancelar el pedido: " + str(e))

# DELETE - Eliminar pedido (devuelve stock automáticamente)
def eliminar(pedido_id):
    try:
        pedido = db.session.get(Pedido, pedido_id)
        if not pedido: raise ValueError("Pedido no encontrado")

        # Devolver stock antes de eliminar
        for detalle in pedido.detalles:
            producto = db.session.get(Producto, detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
                if producto.stock > 0:
                    producto.mostrar = True

        db.session.delete(pedido)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al eliminar el pedido: " + str(e))