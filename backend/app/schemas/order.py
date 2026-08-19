from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ItemPedido(BaseModel):
    producto_id: str = Field(..., example="65cb2f18e4b01a2b3c4d5e6f")
    cantidad: int = Field(..., gt=0, example=2)
    precio_unitario: float = Field(..., gt=0, example=89.99)

class PedidoCreate(BaseModel):
    usuario_id: str = Field(..., example="django_user_12")
    items: List[ItemPedido] = Field(..., min_length=1)

class PedidoResponse(BaseModel):
    id: str = Field(..., alias="_id")
    usuario_id: str
    items: List[ItemPedido]
    total: float = Field(..., gt=0, example=179.98)
    estado: str = Field(default="pendiente", example="pendiente")  # pendiente, procesando, enviado, cancelado
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True
    )