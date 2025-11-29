from app.model import db

"""
Modelo Producto para la tabla 'productos'.
Atributos:
    id (int): Identificador único del producto, clave primaria autoincremental.
    nombre (str): Nombre del producto, no puede ser nulo.
    precio (Decimal): Precio del producto con hasta 10 dígitos y 2 decimales, no puede ser nulo.
    stock (int): Cantidad disponible en inventario, no puede ser nulo.
    categoria (str): Categoría a la que pertenece el producto, no puede ser nulo.
    descripcion (str): Descripción detallada del producto, no puede ser nulo.
    imagen_url (str): URL de la imagen del producto, no puede ser nulo.
    mostrar (bool): Indica si el producto debe mostrarse (por defecto True).
    destacado (bool): Indica si el producto es destacado (por defecto False), no puede ser nulo.
    detalles (list): Relación con los detalles de pedidos asociados a este producto.
Métodos:
    __repr__(): Representación legible del objeto Producto.
"""

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
    destacado = db.Column(db.Boolean, default=False, nullable=False)

    detalles = db.relationship("PedidoDetalle", back_populates="productos", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Producto {self.id} - {self.nombre} - ${self.precio}>"