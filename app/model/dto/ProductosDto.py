from dataclasses import dataclass
from typing import Annotated, Optional
from pydantic import BaseModel, Field

class ProductoEntradaDTO(BaseModel):
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

# DTO para modificar
class ProductoUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    precio: Optional[float] = Field(None, ge=0) # el precio puede ser 0
    stock: Optional[int] = Field(None, ge=0) # el stock puede ser 0
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=1, max_length=200)
    imagen_url: Optional[str] = Field(None, min_length=1, max_length=200)
    mostrar: Optional[bool] = None