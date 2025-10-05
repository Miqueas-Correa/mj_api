from dataclasses import dataclass
from typing import Annotated, Optional
import phonenumbers
from phonenumbers import PhoneNumberFormat, PhoneNumberType
from pydantic import BaseModel, EmailStr, Field, validator
from model.usuarios_model import Usuario

# DTO de ENTRADA
class UsuarioEntradaDTO(BaseModel):
    nombre: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    telefono: str
    contrasenia: Annotated[str, Field(min_length=6, max_length=100)]
    # activo: bool = True
    # rol: Annotated[str, Field(pattern="^(cliente|admin)$")]

    @validator("telefono")
    def validar_telefono(cls, v):
        return validar_telefono_ar(v)

# validacion telefono
def validar_telefono_ar(valor: str) -> str:
    # Si no empieza con +54, se lo agregamos
    if not valor.startswith("+54"):
        valor = "+549" + valor.lstrip("0")  # quita un 0 inicial si lo hubiera

    try:
        parsed = phonenumbers.parse(valor, "AR") # AR es el código de país para Argentina
    except phonenumbers.NumberParseException:
        raise ValueError("Número de teléfono inválido")

    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Número de teléfono inválido")

    # exigir que sea celular
    if phonenumbers.number_type(parsed) not in (PhoneNumberType.MOBILE,
                                                PhoneNumberType.FIXED_LINE_OR_MOBILE):
        raise ValueError("Se requiere un número de teléfono móvil")

    return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)

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

# DTO para modificar usuario
class UsuarioUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr]
    telefono: Optional[str] = Field(None, pattern=r"^\+?\d[\d\s\-]{7,19}$")
    contrasenia: Optional[str] = Field(None, min_length=6, max_length=100)