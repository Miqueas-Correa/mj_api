from flask import Blueprint, request, jsonify
from model.productos_model import db_productos, Producto
# from model.dto.PedidosDTO import 

db_productos = Blueprint("producto", __name__)

# Listar Producto
@db_productos.route("/producto", methods=["GET"])
def listar_productos():
    # muestro la lista de productos en consola para verificar que funciona
    print(Producto.query.all())
    # .query es el acceso al constructor de consultas de SQLAlchemy (Query object).
    # .all() ejecuta la consulta SELECT * FROM pedidos y devuelve una lista de instancias del modelo Producto.
    # Tipo devuelto: (cada elemento es un objeto con atributos como id, id_usuario, codigo_producto, total, fecha, cerrado).
    return jsonify(Producto.query.all()), 200
