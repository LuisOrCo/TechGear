from pydantic import BaseModel, Field

from typing import Optional

class OrderCreate(BaseModel):
    product_id: str | int = Field(..., example="60d5ec49f1a2c81234567890")
    quantity: int = Field(..., gt=0, example=2)
    client_name: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    customer_email: Optional[str] = Field(default=None, example="juan.perez@example.com")
    total: float = Field(..., gt=0, example=500000)

