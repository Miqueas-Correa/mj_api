from flask_sqlalchemy import SQLAlchemy

db_usuarios = SQLAlchemy()

# Definición del modelo de Usuario
class Usuario(db_usuarios.Model):
    __tablename__ = "usuarios"

    id = db_usuarios.Column(db_usuarios.Integer, primary_key=True, autoincrement=True)
    nombre = db_usuarios.Column(db_usuarios.String(100), nullable=False)
    email = db_usuarios.Column(db_usuarios.String(100), unique=True, nullable=False)
    contrasenia = db_usuarios.Column(db_usuarios.String(200), nullable=False)  # cifrada
    telefono = db_usuarios.Column(db_usuarios.String(20), nullable=False)
    activo = db_usuarios.Column(db_usuarios.Boolean, default=True)
    rol = db_usuarios.Column(db_usuarios.Enum("cliente", "admin"), nullable=False)

    # Relación con pedidos (uno a muchos)
    pedidos = db_usuarios.relationship("Pedido", backref="usuario", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.id} - {self.nombre} ({self.rol})>"