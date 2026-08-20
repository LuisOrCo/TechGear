from app.database.connection import db


def create_product(product_data):
    result = db["productos"].insert_one(product_data)

    product_data["_id"] = str(result.inserted_id)

    return product_data