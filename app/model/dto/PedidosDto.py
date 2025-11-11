from typing import List, Optional
from pydantic import BaseModel, Field

"""
Módulos de modelos DTO (Data Transfer Objects) para pedidos.
Contiene definiciones de modelos Pydantic usados para representar y validar
los datos relacionados con pedidos. Estas clases se utilizan para la validación
de entrada en la API y para facilitar la serialización/deserialización de datos
entre capas de la aplicación.
Clases principales:
- PedidoDetalleDTO: Representa una línea de detalle de un pedido (producto y cantidad).
- PedidoUpdateDTO: Representa los campos editables de un pedido para operaciones de actualización.
"""
"""DTO para el detalle de un pedido.
Atributos:
- producto_id (int): Identificador del producto.
- cantidad (int): Cantidad solicitada del producto. Debe ser un entero mayor que 0
    (validado con Field(..., gt=0)).
Uso:
- Representa una línea de pedido en operaciones de creación o actualización de pedidos.
"""
"""DTO para actualización parcial de un pedido.
Todos los campos son opcionales para permitir actualizaciones parciales.
Atributos:
- id_usuario (Optional[int]): Identificador del usuario asociado al pedido.
- cerrado (Optional[bool]): Indicador de si el pedido está cerrado/completado.
- detalles (Optional[List[PedidoDetalleDTO]]): Lista de detalles (líneas) del pedido.
    Si se proporciona, cada elemento debe cumplir la validación definida en PedidoDetalleDTO.
Notas:
- Este DTO está pensado para endpoints de actualización (PATCH/PUT) donde no siempre
    se envían todos los campos del pedido. La validación previa evita estados inválidos.
"""

class PedidoDetalleDTO(BaseModel):
    producto_id: int = Field(None, ge=1)
    cantidad: int = Field(None, gt=0)

class PedidoUpdateDTO(BaseModel):
    id_usuario: Optional[int] = Field(None, ge=1)
    cerrado: Optional[bool] = None
    detalles: Optional[List[PedidoDetalleDTO]] = None