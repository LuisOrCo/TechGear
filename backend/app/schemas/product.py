from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Teclado Mecánico RGB")
    description: str = Field(..., min_length=5, max_length=500, example="Teclado mecánico con retroiluminación RGB y switches mecánicos de alta calidad.")
    price: float = Field(..., gt=0, example=250000)
    stock: int = Field(..., ge=0, example=10)
    category: str = Field(..., min_length=2, max_length=50, example="Periféricos")