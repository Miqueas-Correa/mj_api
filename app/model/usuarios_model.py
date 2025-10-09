from model import db

# Definición del modelo de Usuario
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasenia = db.Column(db.String(512), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    rol = db.Column(db.Enum("cliente", "admin"), nullable=False, default="cliente")

    # Relación con pedidos (uno a muchos)
    pedidos = db.relationship("Pedido", back_populates="usuario", lazy="select")

    def __repr__(self):
        return f"<Usuario {self.id} - {self.nombre} ({self.rol})>"