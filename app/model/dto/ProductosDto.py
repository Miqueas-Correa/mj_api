from dataclasses import dataclass
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class ProductosEntradaDTO(BaseModel):
    nombre: Annotated[str, Field(min_length=1, max_length=100)]
    precio: Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)]
    categoria: Annotated[str, Field(min_length=1, max_length=100)]
    descripcion: Annotated[str, Field(min_length=1, max_length=200)]
    imagen_url: Annotated[str, Field(min_length=1, max_length=150)]
    mostrar: bool = True

@dataclass
class ProductoSalidaDTO:
    id: int
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