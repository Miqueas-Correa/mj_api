from flask import Blueprint, request, jsonify
from model.pedidos_model import db_pedidos, Pedido
# from model.dto.PedidosDTO import 

pedidos_bp = Blueprint("pedidos", __name__)

# Listar pedidos
@pedidos_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    # muestro la lista de pedidos en consola para verificar que funciona
    print(Pedido.query.all())
    # .query es el acceso al constructor de consultas de SQLAlchemy (Query object).
    # .all() ejecuta la consulta SELECT * FROM pedidos y devuelve una lista de instancias del modelo Pedido.
    # Tipo devuelto: (cada elemento es un objeto con atributos como id, id_usuario, codigo_producto, total, fecha, cerrado).
    return jsonify(Pedido.query.all()), 200
