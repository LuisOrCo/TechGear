from fastapi import APIRouter, HTTPException

from app.schemas.order import OrderCreate
from app.services.order_service import (
    create_order,
    get_orders,
    get_order_by_id,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/")
def create_new_order(order: OrderCreate):
    return create_order(order.model_dump())

@router.get("/")
def get_all_orders():
    return get_orders()

@router.get("/{order_id}")
def get_order(order_id: str):
    order = get_order_by_id(order_id)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return order