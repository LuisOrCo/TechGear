from fastapi import APIRouter

from app.schemas.product import ProductCreate
from app.services.product_service import create_product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
def create_new_product(product: ProductCreate):
    return create_product(product.model_dump())