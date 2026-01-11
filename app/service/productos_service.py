from app.model.dto.ProductosDTO import ProductoSalidaDTO
from app.model.productos_model import Producto
from app.extensions import db
"""
Servicio para la gestión de productos.
Funciones:
-----------
listar():
    Obtiene una lista de todos los productos visibles (mostrar=True).
    Devuelve una lista de diccionarios con los datos de cada producto.
obtener(by, valor):
    Busca productos según el criterio especificado:
        - by=0: Busca productos cuyo nombre contenga el valor dado (case-insensitive).
        - by=1: Busca producto por ID (devuelve aunque esté oculto).
        - by=2: Busca productos por categoría (case-insensitive).
    Devuelve una lista de diccionarios con los datos de los productos encontrados.
    Lanza ValueError si no se encuentran productos o si el parámetro 'by' es inválido.
categorias_list():
    Obtiene una lista de todas las categorías distintas de los productos.
    Devuelve una lista de strings con los nombres de las categorías.
featured():
    Lista todos los productos destacados (destacado=True y mostrar=True).
    Devuelve una lista de diccionarios con los datos de los productos destacados.
actualizar_stock(producto_id, cantidad):
    Actualiza el stock de un producto identificado por su ID.
    Si el stock es menor o igual a 0, el producto se oculta (mostrar=False).
    Si el stock es mayor a 0, el producto se muestra (mostrar=True).
    Devuelve un diccionario con los datos actualizados del producto.
    Lanza ValueError si el producto no existe o si ocurre un error al actualizar.
"""

# PARA EL METODO GET
def listar():
    try:
        productos = Producto.query.filter_by(mostrar=True).all()

        return [ProductoSalidaDTO.from_model(u).__dict__ for u in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos: " + str(e))

# buscar productos por id, por nombre o categoria
def obtener(by, valor):
    try:
        if by not in [0, 1, 2]: raise ValueError("Error en el parámetro 'by' debe ser 0, 1 o 2")

        if by == 1:
            producto = db.session.get(Producto, valor)
            if not producto: raise ValueError(f"Producto {valor} no fue encontrado")
            # IMPORTANTE: Al buscar por ID, devolver el producto aunque esté oculto
            # Esto permite ver detalles de pedidos con productos que ya no están disponibles
            return [ProductoSalidaDTO.from_model(producto).__dict__]

        elif by == 0:
            productos = Producto.query.filter(Producto.nombre.like(f"%{valor}%")).all()
            if not productos: raise ValueError(f"No se encontraron productos con nombre similar a '{valor}'")

        else:  # by == 2
            productos = Producto.query.filter(db.func.lower(Producto.categoria) == valor.lower()).all()
            if not productos: raise ValueError(f"No se encontraron productos en la categoría '{valor}'")

        # Solo filtrar por mostrar=True cuando NO se busca por ID
        productos = [p for p in productos if p.mostrar == True]

        if not productos: raise ValueError("No se encontraron productos")

        return [ProductoSalidaDTO.from_model(p).__dict__ for p in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos: " + str(e))

# buscar todas las categorias de los productos
def categorias_list():
    try:
        categorias = db.session.query(Producto.categoria).distinct().all()
        return [c[0] for c in categorias] if categorias is not None else []
    except Exception as e:
        raise ValueError("Error al listar categorías: " + str(e))

# Lista todos los productos destacados
def featured():
    try:
        query = Producto.query.filter_by(destacado=True)
        query = query.filter_by(mostrar=True)
        productos = query.all()
        return [ProductoSalidaDTO.from_model(p).__dict__ for p in productos]
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError("Error al listar productos destacados: " + str(e))

# Actualizar stock de un producto
def actualizar_stock(producto_id, cantidad):
    try:
        producto = db.session.get(Producto, producto_id)
        if not producto:
            raise ValueError(f"Producto {producto_id} no encontrado")

        producto.stock = cantidad

        # Ocultar/mostrar según stock
        if cantidad <= 0:
            producto.mostrar = False
        else:
            producto.mostrar = True

        db.session.commit()

        return ProductoSalidaDTO.from_model(producto).__dict__

    except Exception as e:
        db.session.rollback()
        raise ValueError("Error al actualizar stock: " + str(e))