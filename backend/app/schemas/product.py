from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Teclado Mecánico RGB")
    descripcion: str = Field(..., max_length=500, example="Switch Red, formato 75%, retroiluminado")
    precio: float = Field(..., gt=0, example=89.99)
    stock: int = Field(..., ge=0, example=25)
    categoria: str = Field(..., example="Periféricos")
    imagen_url: Optional[str] = Field(default=None, example="https://ejemplo.com/imagen.jpg")

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    categoria: Optional[str] = None
    imagen_url: Optional[str] = None

class ProductoResponse(ProductoBase):
    id: str = Field(..., alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "65cb2f18e4b01a2b3c4d5e6f",
                "nombre": "Teclado Mecánico RGB",
                "descripcion": "Switch Red, formato 75%, retroiluminado",
                "precio": 89.99,
                "stock": 25,
                "categoria": "Periféricos",
                "imagen_url": "https://ejemplo.com/imagen.jpg"
            }
        }
    )