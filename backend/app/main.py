from fastapi import FastAPI

app = FastAPI(
    tittle="TechGear API",
    description="API para gestionar productos y pedidos de TechGear",
    version="1.0.0"
)

@app.get("/")
def Inicio():
    return {
        "mensaje":"Bienvenido a la API de TechGear."
    }