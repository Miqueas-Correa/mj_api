from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductoDTO:
    id: Optional[int]
    nombre: str
    precio: float
    stock: int
    categoria: str
    descripcion: str
    imagen_url: str
    mostrar: bool

    @classmethod
    def from_model(cls, producto):
        return cls(
            id=producto.id,
            nombre=producto.nombre,
            precio=float(producto.precio),
            stock=producto.stock,
            categoria=producto.categoria,
            descripcion=producto.descripcion,
            imagen_url=producto.imagen_url,
            mostrar=producto.mostrar
        )