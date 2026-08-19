from fastapi import FastAPI

from app.database.connection import client


app = FastAPI(
    title="TechGear API",
    description="API para gestionar productos y pedidos de TechGear",
    version="1.0.0"
)


@app.get("/")
def inicio():
    try:
        client.admin.command("ping")

        return {
            "mensaje": "Bienvenido a la API de TechGear",
            "mongodb": "Conectado correctamente"
        }

    except Exception as e:
        return {
            "mensaje": "Bienvenido a la API de TechGear",
            "mongodb": "Error de conexión",
            "error": str(e)
        }