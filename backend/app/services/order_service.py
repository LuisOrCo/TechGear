from bson import ObjectId

from app.database.connection import db

def create_order(order_data):
    result = db["pedidos"].insert_one(order_data)

    order_data["_id"] = str(result.inserted_id)

    return order_data

def get_orders():
    orders = list(db["pedidos"].find())

    for order in orders:
        order["_id"] = str(order["_id"])

    return orders