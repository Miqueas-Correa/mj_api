from model import db

# Definición del modelo de productos
class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(200), nullable=False)
    mostrar = db.Column(db.Boolean, default=True)

    # Relación con pedidos (uno a muchos)
    pedidos = db.relationship("Pedido", back_populates="producto", lazy="select")

    def __repr__(self):
        return f"<Producto {self.id} - {self.nombre} - ${self.precio}>"