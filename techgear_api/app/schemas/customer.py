from pydantic import BaseModel, EmailStr


from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre del cliente",
        json_schema_extra={"example": "Juan"},
    )
    lastname: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Apellido del cliente",
        json_schema_extra={"example": "Pérez"},
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico válido",
        json_schema_extra={"example": "juan.perez@example.com"},
    )
    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
        pattern=r"^\+?[0-9\s\-]+$",
        description="Número de teléfono de contacto",
        json_schema_extra={"example": "+573001234567"},
    )
    address: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Dirección de residencia o entrega",
        json_schema_extra={"example": "Calle 10 # 40-20, Medellín"},
    )