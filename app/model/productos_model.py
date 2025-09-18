from flask_sqlalchemy import SQLAlchemy

db_productos = SQLAlchemy()

# Definición del modelo de productos
class Producto(db_productos.Model):
    __tablename__ = "productos"

    id = db_productos.Column(db_productos.Integer, primary_key=True, autoincrement=True)
    nombre = db_productos.Column(db_productos.String(100), nullable=False)
    precio = db_productos.Column(db_productos.Numeric(10, 2), nullable=False)
    stock = db_productos.Column(db_productos.Integer, nullable=False)
    categoria = db_productos.Column(db_productos.String(50), nullable=False)
    descripcion = db_productos.Column(db_productos.Text, nullable=False)
    imagen_url = db_productos.Column(db_productos.String(200), nullable=False)
    mostrar = db_productos.Column(db_productos.Boolean, default=True)

    # Relación con pedidos (uno a muchos)
    pedidos = db_productos.relationship("Pedido", backref="producto", lazy=True)

    def __repr__(self):
        return f"<Producto {self.id} - {self.nombre} - ${self.precio}>"
