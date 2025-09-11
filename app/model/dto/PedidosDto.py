from dataclasses import dataclass
from typing import Optional

@dataclass
class PedidoDTO:
    id: Optional[int]
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
