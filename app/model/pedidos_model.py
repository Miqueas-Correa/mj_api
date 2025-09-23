from datetime import datetime, timezone
from model import db

# Definición del modelo de pedidos
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    codigo_producto = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    cerrado = db.Column(db.Boolean, default=False)

    # Relaciones (para acceder a los objetos completos)
    usuario = db.relationship("Usuario", back_populates="pedidos", lazy="joined")
    producto = db.relationship("Producto", back_populates="pedidos", lazy="joined")

    def __repr__(self):
        return f"<Pedido {self.id} - Usuario {self.id_usuario} - Producto {self.codigo_producto}>"