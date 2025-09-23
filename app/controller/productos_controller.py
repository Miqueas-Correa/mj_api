from flask import Blueprint, request, jsonify
from model.dto.ProductosDTO import ProductoSalidaDTO
from model.productos_model import db, Producto
# from model.dto.PedidosDTO import 

productos_bp = Blueprint("productos", __name__)

# Listar Producto
@productos_bp.route("/productos", methods=["GET"])
def listar_productos():
    productos = Producto.query.all()
    print(productos)
    # .query es el acceso al constructor de consultas de SQLAlchemy (Query object).
    # .all() ejecuta la consulta SELECT * FROM pedidos y devuelve una lista de instancias del modelo Producto.
    # Tipo devuelto: (cada elemento es un objeto con atributos como id, id_usuario, codigo_producto, total, fecha, cerrado).
    return jsonify([ProductoSalidaDTO.from_model(p).__dict__ for p in productos]), 200
