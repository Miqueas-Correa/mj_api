from app.model.dto.ProductosDTO import ProductoSalidaDTO
from app.model.productos_model import Producto
from app.extensions import db

"""
Módulo de servicios para la gestión de productos.
Funciones:
    listar(L_mostrar):
        Lista todos los productos, permitiendo filtrar por el atributo 'mostrar'.
        Parámetros:
            L_mostrar (str | None): Si es 'true', muestra solo productos activos; si es 'false', solo inactivos; si es None, muestra todos.
        Retorna:
            Lista de diccionarios con los datos de los productos.
        Excepciones:
            ValueError: Si el parámetro 'mostrar' es inválido o ocurre un error al listar.
    obtener(by, valor, L_mostrar):
        Busca productos por ID, nombre o categoría, con opción de filtrar por 'mostrar'.
        Parámetros:
            by (int): 0 para buscar por nombre, 1 por ID, 2 por categoría.
            valor (str | int): Valor a buscar.
            L_mostrar (str | None): Filtro por el atributo 'mostrar'.
        Retorna:
            Lista de diccionarios con los datos de los productos encontrados.
        Excepciones:
            ValueError: Si los parámetros son inválidos o no se encuentran productos.
    categorias_list():
        Obtiene la lista de categorías distintas de los productos.
        Retorna:
            Lista de nombres de categorías.
        Excepciones:
            ValueError: Si ocurre un error al listar las categorías.
    featured(L_mostrar):
        Lista todos los productos destacados, con opción de filtrar por 'mostrar'.
        Parámetros:
            L_mostrar (str | None): Filtro por el atributo 'mostrar'.
        Retorna:
            Lista de diccionarios con los datos de los productos destacados.
        Excepciones:
            ValueError: Si el parámetro es inválido o ocurre un error al listar.
    crear(request):
        Crea un nuevo producto a partir de los datos recibidos.
        Parámetros:
            request (dict): Datos del producto a crear.
        Excepciones:
            ValueError: Si los datos son inválidos o ya existe un producto con ese nombre.
            RuntimeError: Si ocurre un error inesperado al crear el producto.
    editar(valor, request):
        Modifica los datos de un producto existente.
        Parámetros:
            valor (int): ID del producto a modificar.
            request (dict): Datos a actualizar.
        Excepciones:
            ValueError: Si los datos son inválidos, el producto no existe o no se pudo modificar.
    eliminar(valor):
        Elimina un producto por su ID.
        Parámetros:
            valor (int): ID del producto a eliminar.
        Retorna:
            dict: Mensaje de éxito.
        Excepciones:
            ValueError: Si el producto no existe o ocurre un error al eliminar.
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
            productos = [producto]

        elif by == 0:
            productos = Producto.query.filter(Producto.nombre.like(f"%{valor}%")).all()
            if not productos: raise ValueError(f"No se encontraron productos con nombre similar a '{valor}'")

        else:  # by == 2
            productos = Producto.query.filter(db.func.lower(Producto.categoria) == valor.lower()).all()
            if not productos: raise ValueError(f"No se encontraron productos en la categoría '{valor}'")

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