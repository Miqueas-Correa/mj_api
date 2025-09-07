from dataclasses import dataclass
from typing import Optional

@dataclass
class UsuarioDTO:
    id: Optional[int]
    nombre: str
    email: str
    telefono: str
    activo: bool
    rol: str

    @classmethod
    def from_model(cls, usuario):
        return cls(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            telefono=usuario.telefono,
            activo=usuario.activo,
            rol=usuario.rol
        )