from pydantic import ValidationError
from model.dto.PedidosDTO import PedidoSalidaDTO, PedidoEntradaDTO, PedidoUpdateDTO
from model.pedidos_model import Pedido, db

# PARA EL METODO GET
def listar(L_cerrado):
    try:
        if L_cerrado is not None:
            if L_cerrado.lower() == 'true':
                pedidos = Pedido.query.filter_by(cerrado=True).all()
            elif L_cerrado.lower() == 'false':
                pedidos = Pedido.query.filter_by(cerrado=False).all()
            else:
                raise ValueError("Error en el parámetro 'cerrado' debe ser 'true' o 'false'")
        else:
            pedidos = Pedido.query.all()
        return [PedidoSalidaDTO.from_model(u).__dict__ for u in pedidos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar pedidos: " + str(e))

# buscar pedidos por id, por id usuario o codigo producto
# si by es 1 busca por id, si es 0 busca por id usuario, si es 2 busca por codigo producto
def obtener(by, valor, L_cerrado):
    try:
        # si by no contiene 0,1 o 2 lanza error
        if by not in [0, 1, 2]: raise ValueError("Error en el parámetro 'by' debe ser 0, 1 o 2")

        if by == 1:
            pedido = Pedido.query.get(valor)
            if not pedido: raise ValueError(f"Producto {valor} no fue encontrado")
            pedidos = [pedido]

        elif by == 0:
            pedidos = Pedido.query.filter(Pedido.id_usuario.like(f"%{valor}%")).all()
            if not pedidos: raise ValueError(f"No se encontraron pedidos con el id usuario similar a: '{valor}'")

        else:  # by == 2
            pedidos = Pedido.query.filter_by(codigo_producto=valor).all()
            if not pedidos: raise ValueError(f"No se encontraron pedidos con el codigo producto: '{valor}'")

        # Filtrar según L_cerrado
        if L_cerrado is not None:
            if L_cerrado.lower() not in ['true', 'false']:
                raise ValueError("Error en el parámetro 'cerrado', debe ser 'true' o 'false'")

            mostrar_cerrados = L_cerrado.lower() == 'true'
            pedidos = [p for p in pedidos if p.cerrado == mostrar_cerrados]

            if not pedidos:
                raise ValueError("No se encontraron pedidos que coincidan con el filtro 'cerrado'")

        # Convertir a DTOs
        # Si hay uno solo, devolvemos el objeto directamente
        return [PedidoSalidaDTO.from_model(p).__dict__ for p in pedidos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar pedidos: " + str(e))

# PARA EL METODO POST
def crear(request):
    try:
        dto = PedidoEntradaDTO(**request)

        # Creo el pedido
        nuevo_pedido = Pedido(
            id_usuario=dto.id_usuario,
            codigo_producto=dto.codigo_producto,
            total=dto.total
        )

        db.session.add(nuevo_pedido) # prepara la insercion
        db.session.commit() # ejecuta la insercion en la base de datos
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error inesperado al crear el pedido: {str(e)}")

# PARA EL METODO PUT
def editar(valor, request):
    try:
        # busco por id
        pedido = Pedido.query.get(valor)

        if not pedido: raise ValueError("Pedido no encontrado")

        dto = PedidoUpdateDTO(**request)
        if not any([dto.id_usuario, dto.codigo_producto, dto.total, dto.cerrado]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False
        # Actualizar los campos
        if dto.id_usuario is not None:
            pedido.id_usuario = dto.id_usuario
            modificado = True

        if dto.total < 0:
            raise ValueError("El total no puede ser negativo")
        else:
            pedido.total = dto.total
            modificado = True

        if dto.codigo_producto is not None:
            pedido.codigo_producto = dto.codigo_producto
            modificado = True

        if dto.cerrado is not None:
            pedido.cerrado = dto.cerrado
            modificado = True

        if not modificado:
            raise ValueError("No se pudo modificar el pedido")
        # Guardar los cambios en la base de datos
        db.session.commit()
    except ValidationError as e:
        db.session.rollback()
        raise ValueError("Error de validación: " + str(e))
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()  # Revertir cambios en caso de error
        raise ValueError("Error al modificar el pedido: " + str(e))

# PARA EL METODO DELETE
def eliminar(valor):
    try:
        # busco por id
        pedido = Pedido.query.get(valor)
        if not pedido: raise ValueError("Pedido no encontrado")
        db.session.delete(pedido)
        db.session.commit()
        return {"message": "Pedido eliminado exitosamente"}
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()  # Revertir cambios en caso de error
        raise ValueError("Error al eliminar el pedido: " + str(e))