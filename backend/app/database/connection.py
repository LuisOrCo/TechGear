import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    client = MongoClient(MONGODB_URL)

    client.admin.command("ping")

    db = client[DATABASE_NAME]

    print("✅ Conexión exitosa a MongoDB")
    print(f"📦 Base de datos: {DATABASE_NAME}")

except Exception as e:
    print("❌ Error:")
    print(e)