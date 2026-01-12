from typing import List, Optional
from pydantic import BaseModel, Field
"""
DTOs para la gestión de pedidos.
Clases:
    PedidoDetalleDTO: Representa el detalle de un producto dentro de un pedido, incluyendo el ID del producto y la cantidad solicitada.
    PedidoUpdateDTO: Utilizado para actualizar un pedido existente, permitiendo modificar el usuario asociado, el estado de cerrado y la lista de detalles del pedido.
Atributos:
    PedidoDetalleDTO:
        producto_id (int): Identificador único del producto. Debe ser mayor o igual a 1.
        cantidad (int): Cantidad del producto solicitada. Debe ser mayor que 0.
    PedidoUpdateDTO:
        id_usuario (Optional[int]): Identificador del usuario asociado al pedido. Opcional y debe ser mayor o igual a 1 si se proporciona.
        cerrado (Optional[bool]): Indica si el pedido está cerrado. Opcional.
        detalles (Optional[List[PedidoDetalleDTO]]): Lista de detalles del pedido. Opcional.
"""

class PedidoDetalleDTO(BaseModel):
    producto_id: int = Field(None, ge=1)
    cantidad: int = Field(None, gt=0)

class PedidoUpdateDTO(BaseModel):
    id_usuario: Optional[int] = Field(None, ge=1)
    cerrado: Optional[bool] = None
    detalles: Optional[List[PedidoDetalleDTO]] = None