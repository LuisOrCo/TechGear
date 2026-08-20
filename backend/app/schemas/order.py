from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    product_id: int = Field(..., gt=0, example=1)
    quantity: int = Field(..., gt=0, example=2)
    client_name: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    total: float = Field(..., gt=0, example=500000)
