from fastapi import APIRouter, HTTPException

from app.schemas.product import ProductCreate
from app.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
def create_new_product(product: ProductCreate):
    return create_product(product.model_dump())


@router.get("/")
def get_all_products():
    return get_products()


@router.get("/{product_id}")
def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}")
def update_existing_product(product_id: str, product: ProductCreate):
    updated_product = update_product(
        product_id,
        product.model_dump()
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product


@router.delete("/{product_id}")
def delete_existing_product(product_id: str):
    deleted = delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }