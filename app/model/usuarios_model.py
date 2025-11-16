from app.model import db

"""
Modelo de datos para la entidad Usuario.
Atributos:
    id (int): Identificador único del usuario, clave primaria autoincremental.
    nombre (str): Nombre completo del usuario. No puede ser nulo.
    email (str): Correo electrónico del usuario. Debe ser único y no nulo.
    contrasenia (str): Contraseña cifrada del usuario. No puede ser nula.
    telefono (str): Número de teléfono del usuario. No puede ser nulo.
    activo (bool): Indica si el usuario está activo. Por defecto es True.
    rol (Enum): Rol del usuario, puede ser "cliente" o "admin". Por defecto es "cliente".
    pedidos (list): Relación uno a muchos con el modelo Pedido. Al eliminar un usuario, se eliminan sus pedidos asociados.
Métodos:
    __repr__(): Representación legible del objeto Usuario, mostrando id, nombre y rol.
"""

# Definición del modelo de Usuario
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasenia = db.Column(db.String(250), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rol = db.Column(db.Enum("cliente", "admin"), nullable=False, default="cliente")

    pedidos = db.relationship("Pedido", back_populates="usuarios", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario {self.id} - {self.nombre} ({self.rol})>"