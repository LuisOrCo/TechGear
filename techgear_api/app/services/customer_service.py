from app.database.connection import db


def create_customer(customer_data):
    result = db["clientes"].insert_one(customer_data)

    customer_data["_id"] = str(result.inserted_id)

    return customer_data

def get_customers():
    customers = list(db["clientes"].find())

    for customer in customers:
        customer["_id"] = str(customer["_id"])

    return customers