from datetime import UTC, datetime
from app.extensions import db

"""
Definición de los modelos de base de datos para la gestión de pedidos y sus detalles.
Clases:
    Pedido:
        Representa un pedido realizado por un usuario.
        Atributos:
            id (int): Identificador único del pedido.
            id_usuario (int): Identificador del usuario que realizó el pedido.
            fecha (datetime): Fecha y hora en que se realizó el pedido.
            total (float): Monto total del pedido.
            cerrado (bool): Indica si el pedido está cerrado o no.
            detalles (list[PedidoDetalle]): Lista de detalles asociados al pedido.
            usuarios (Usuario): Relación con el usuario que realizó el pedido.
    PedidoDetalle:
        Representa el detalle de un producto dentro de un pedido.
        Atributos:
            id (int): Identificador único del detalle.
            pedido_id (int): Identificador del pedido al que pertenece el detalle.
            producto_id (int): Identificador del producto incluido en el pedido.
            cantidad (int): Cantidad del producto en el pedido.
            pedidos (Pedido): Relación con el pedido asociado.
            productos (Producto): Relación con el producto asociado.
"""

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    total = db.Column(db.Float, nullable=False)
    cerrado = db.Column(db.Boolean, default=False)

    detalles = db.relationship("PedidoDetalle", back_populates="pedidos", cascade="all, delete-orphan")
    usuarios = db.relationship("Usuario", back_populates="pedidos", lazy="select")
class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    pedidos = db.relationship("Pedido", back_populates="detalles", lazy="select")
    productos = db.relationship("Producto")