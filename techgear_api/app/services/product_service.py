from bson import ObjectId

from app.database.connection import db


def create_product(product_data):
    result = db["productos"].insert_one(product_data)

    product_data["_id"] = str(result.inserted_id)

    return product_data


def get_products():
    products = list(db["productos"].find())

    for product in products:
        product["_id"] = str(product["_id"])

    return products


def get_product_by_id(product_id: str):
    if not ObjectId.is_valid(product_id):
        return None
    product = db["productos"].find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
    return product


def update_product(product_id, product_data):
    result = db["productos"].update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product_data}
    )

    if result.matched_count == 0:
        return None

    updated_product = db["productos"].find_one(
        {"_id": ObjectId(product_id)}
    )

    updated_product["_id"] = str(updated_product["_id"])

    return updated_product


def delete_product(product_id):
    result = db["productos"].delete_one(
        {"_id": ObjectId(product_id)}
    )

    return result.deleted_count > 0