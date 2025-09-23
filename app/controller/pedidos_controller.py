from flask import Blueprint, request, jsonify
from model.dto.PedidosDTO import PedidoSalidaDTO
from model.pedidos_model import db, Pedido
# from model.dto.PedidosDTO import 

pedidos_bp = Blueprint("pedidos", __name__)

# Listar pedidos
@pedidos_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = Pedido.query.all()
    print(pedidos)
    # .query es el acceso al constructor de consultas de SQLAlchemy (Query object).
    # .all() ejecuta la consulta SELECT * FROM pedidos y devuelve una lista de instancias del modelo Pedido.
    # Tipo devuelto: (cada elemento es un objeto con atributos como id, id_usuario, codigo_producto, total, fecha, cerrado).
    return jsonify([PedidoSalidaDTO.from_model(p).__dict__ for p in pedidos]), 200