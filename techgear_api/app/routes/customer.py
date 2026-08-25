from fastapi import APIRouter
from app.schemas.customer import CustomerCreate
from app.services.customer_service import create_customer, get_customers


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/")
def create_new_customer(customer: CustomerCreate):
    return create_customer(customer.model_dump())


@router.get("/")
def get_all_customers():
    return get_customers()