from pydantic import ValidationError
from model.dto.ProductosDTO import ProductoSalidaDTO, ProductoEntradaDTO, ProductoUpdateDTO
from model.productos_model import Producto, db

# PARA EL METODO GET
def listar(L_mostrar):
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
# si by es 1 busca por id, si es 0 busca por nombre, si es 2 busca por categoria
def obtener(by, valor, L_mostrar):
    try:
        # si by no contiene 0,1 o 2 lanza error
        if by not in [0, 1, 2]: raise ValueError("Error en el parámetro 'by' debe ser 0, 1 o 2")

        if by == 1:
            producto = Producto.query.get(valor)
            if not producto: raise ValueError(f"Producto {valor} no fue encontrado")
            productos = [producto]

        elif by == 0:
            productos = Producto.query.filter(Producto.nombre.like(f"%{valor}%")).all()
            if not productos: raise ValueError(f"No se encontraron productos con nombre similar a '{valor}'")

        else:  # by == 2
            productos = Producto.query.filter_by(categoria=valor).all()
            if not productos: raise ValueError(f"No se encontraron productos en la categoría '{valor}'")

        # Filtrar según L_mostrar
        if L_mostrar is not None:
            if L_mostrar.lower() not in ['true', 'false']:
                raise ValueError("Error en el parámetro 'mostrar', debe ser 'true' o 'false'")

            mostrar_activos = L_mostrar.lower() == 'true'
            productos = [p for p in productos if p.mostrar == mostrar_activos]

            if not productos:
                raise ValueError("No se encontraron productos que coincidan con el filtro 'mostrar'")

        # Convertir a DTOs
        # Si hay uno solo, devolvemos el objeto directamente
        return [ProductoSalidaDTO.from_model(p).__dict__ for p in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos: " + str(e))

# PARA EL METODO POST
def crear(request):
    try:
        dto = ProductoEntradaDTO(**request)
        # nombre unico
        if Producto.query.filter_by(nombre=dto.nombre).first():
            raise ValueError("Ya existe un producto con ese nombre")

        # Si pasa, creo el producto
        nuevo_producto = Producto(
            nombre=dto.nombre,
            precio=dto.precio,
            stock=dto.stock,
            categoria=dto.categoria,
            descripcion=dto.descripcion,
            imagen_url=dto.imagen_url,
            mostrar=dto.mostrar
        )

        db.session.add(nuevo_producto) # prepara la insercion
        db.session.commit() # ejecuta la insercion en la base de datos
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e.errors()}")
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error inesperado al crear el producto: {str(e)}")

# PARA EL METODO PUT
def editar(valor, request, by_id):
    try:
        # busco por id o por nombre
        producto = Producto.query.get(valor) if by_id else Producto.query.filter_by(nombre=valor).first()

        if not producto: raise ValueError("Producto no encontrado")

        dto = ProductoUpdateDTO(**request)
        if not any([dto.nombre, dto.precio, dto.stock, dto.categoria,
                    dto.descripcion, dto.imagen_url, dto.mostrar]):
            raise ValueError("No se proporcionaron datos para actualizar")

        modificado = False
        # Actualizar los campos
        if dto.nombre is not None:
            # Verificar si el nuevo nombre ya está en uso por otro
            if producto.nombre != dto.nombre and Producto.query.filter_by(nombre=dto.nombre).first():
                raise ValueError("El nombre de usuario ya está registrado")
            producto.nombre = dto.nombre
            modificado = True

        if dto.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        else:
            producto.precio = dto.precio
            modificado = True

        if dto.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        else:
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

        if not modificado:
            raise ValueError("No se pudo modificar el producto")
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
        raise ValueError("Error al modificar el producto: " + str(e))

# PARA EL METODO DELETE
def eliminar(valor, by_id):
    try:
        # busco por id o por nombre
        producto = Producto.query.get(valor) if by_id else Producto.query.filter_by(nombre=valor).first()
        if not producto: raise ValueError("Producto no encontrado")
        db.session.delete(producto)
        db.session.commit()
        return {"message": "Producto eliminado exitosamente"}
    except ValueError as e:
        db.session.rollback()
        raise
    except Exception as e:
        db.session.rollback()  # Revertir cambios en caso de error
        raise ValueError("Error al eliminar el producto: " + str(e))