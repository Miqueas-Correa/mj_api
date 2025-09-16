from dataclasses import dataclass
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field
from model.usuarios_model import Usuario

# DTO de ENTRADA
class UsuarioEntradaDTO(BaseModel):
    nombre: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    telefono: Annotated[str, Field(pattern=r"^\+?\d[\d\s\-]{7,19}$")]
    contrasenia: Annotated[str, Field(min_length=6, max_length=100)]
    activo: bool = True
    rol: Annotated[str, Field(pattern="^(cliente|admin)$")]

# DTO de SALIDA (evitamos devolver contrasenia)
@dataclass
class UsuarioSalidaDTO:
    id: int
    nombre: str
    email: str
    telefono: str
    activo: bool
    rol: str

    @classmethod
    def from_model(cls, usuario: Usuario):
        return cls(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            telefono=usuario.telefono,
            activo=usuario.activo,
            rol=usuario.rol
        )