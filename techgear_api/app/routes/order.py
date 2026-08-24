from fastapi import APIRouter, HTTPException

from app.schemas.order import OrderCreate
from app.services.order_service import (
    create_order,
    get_orders,)

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