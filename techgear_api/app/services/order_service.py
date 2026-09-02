from bson import ObjectId
from fastapi import HTTPException

from app.database.connection import db


def create_order(order_data):
    product_id = order_data.get("product_id")
    quantity = order_data.get("quantity", 1)

    # 1. Verificar si el producto existe en MongoDB
    product = None
    if isinstance(product_id, str) and ObjectId.is_valid(product_id):
        product = db["productos"].find_one({"_id": ObjectId(product_id)})

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"El producto con ID '{product_id}' no existe."
        )

    # 2. Verificar disponibilidad de stock
    available_stock = product.get("stock", 0)
    if available_stock <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"El producto '{product.get('name')}' se encuentra agotado."
        )

    if quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente. Stock disponible: {available_stock}, solicitado: {quantity}."
        )

    # 3. Insertar el pedido en la colección 'pedidos'
    result = db["pedidos"].insert_one(order_data)
    order_data["_id"] = str(result.inserted_id)

    # 4. Descontar el stock en la colección 'productos'
    db["productos"].update_one(
        {"_id": product["_id"]},
        {"$inc": {"stock": -quantity}}
    )

    return order_data


def get_orders():
    orders = list(db["pedidos"].find())

    for order in orders:
        order["_id"] = str(order["_id"])

    return orders


def get_order_by_id(order_id: str):
    if not ObjectId.is_valid(order_id):
        return None
    order = db["pedidos"].find_one({"_id": ObjectId(order_id)})
    if order:
        order["_id"] = str(order["_id"])
    return order