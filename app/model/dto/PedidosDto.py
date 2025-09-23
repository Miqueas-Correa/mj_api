from dataclasses import dataclass
from typing import Annotated, Optional

from pydantic import BaseModel, Field

class PedidosEntradaDTO(BaseModel):
    id_usuario: Annotated[int, Field(ge=1)]
    codigo_producto: Annotated[int, Field(ge=1)]
    total: Annotated[float, Field(gt=0)]

@dataclass
class PedidoSalidaDTO:
    id: int
    id_usuario: int
    codigo_producto: int
    total: float

    @classmethod
    def from_model(cls, pedido):
        return cls(
            id=pedido.id,
            id_usuario=pedido.id_usuario,
            codigo_producto=pedido.codigo_producto,
            total=float(pedido.total)
        )
