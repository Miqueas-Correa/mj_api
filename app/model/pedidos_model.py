from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db_pedidos = SQLAlchemy()

# Definición del modelo de pedidos
class Pedido(db_pedidos.Model):
    __tablename__ = "pedidos"

    id = db_pedidos.Column(db_pedidos.Integer, primary_key=True, autoincrement=True)
    id_usuario = db_pedidos.Column(db_pedidos.Integer, db_pedidos.ForeignKey("usuarios.id"), nullable=False)
    codigo_producto = db_pedidos.Column(db_pedidos.Integer, db_pedidos.ForeignKey("productos.id"), nullable=False)
    total = db_pedidos.Column(db_pedidos.Numeric(10, 2), nullable=False)
    fecha = db_pedidos.Column(db_pedidos.DateTime, default=lambda: datetime.now(timezone.utc))
    cerrado = db_pedidos.Column(db_pedidos.Boolean, default=False)

    # Relaciones (para acceder a los objetos completos)
    usuario = db_pedidos.relationship("Usuario", backref="pedidos", lazy=True)
    producto = db_pedidos.relationship("Producto", backref="pedidos", lazy=True)

    def __repr__(self):
        return f"<Pedido {self.id} - Usuario {self.id_usuario} - Producto {self.codigo_producto}>"