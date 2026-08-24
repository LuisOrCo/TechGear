# TechGear

TechGear es una tienda especializada en hardware y accesorios tecnológicos. El proyecto utiliza una API desarrollada con **FastAPI** para gestionar productos y pedidos, junto con una aplicación web desarrollada con **Django** para renderizar la interfaz desde el servidor.

## Tecnologías

* **Python**
* **FastAPI** — API Backend
* **Django** — Aplicación Web / MVT
* **MongoDB Atlas** — Base de datos
* **httpx** — Consumo de la API desde Django
* **Uvicorn** — Servidor de desarrollo para FastAPI

## Estructura del proyecto

```text
TechGear/
│
├── techgear_api/                       # API Backend (FastAPI)
│   ├── app/
│   │   ├── database/                   # Configuración y conexión a la base de datos
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   │
│   │   ├── routes/                     # Endpoints de la API
│   │   │   ├── __init__.py
│   │   │   ├── order.py
│   │   │   └── product.py
│   │   │
│   │   ├── schemas/                    # Modelos Pydantic
│   │   │   ├── __init__.py
│   │   │   ├── order.py
│   │   │   └── product.py
│   │   │
│   │   ├── services/                   # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── order_service.py
│   │   │   └── product_service.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py                     # Punto de entrada de FastAPI
│   │
│   └── .env                            # Variables de entorno
│
├── techgear_web/                       # Aplicación Web (Django)
│   ├── catalog/
│   │   ├── migrations/
│   │   ├── templates/                  # Plantillas HTML
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── config/                         # Configuración de Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── db.sqlite3
│   └── manage.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación

Clonar el repositorio y acceder al proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd TechGear
```

Crear y activar el entorno virtual:

```bash
python -m venv venv
```

En Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Variables de entorno

El Backend utiliza un archivo `.env` dentro de `techgear_api/` para almacenar las variables de conexión a MongoDB Atlas.

Ejemplo:

```env
MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>/
DATABASE_NAME=techgear
```

**No se deben publicar las credenciales reales de MongoDB Atlas.** El archivo `.env` debe estar incluido en `.gitignore`.

## Ejecutar el Backend

Primero, desde la raíz del proyecto, acceder a la carpeta del Backend:

```powershell
cd techgear_api
```

Con el entorno virtual activo, ejecutar:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## Ejecutar Django

Abrir una **segunda terminal**, activar el entorno virtual y acceder a la aplicación web:

```powershell
cd TechGear
.\venv\Scripts\Activate.ps1
cd techgear_web
```

Ejecutar Django en un puerto diferente al de FastAPI:

```powershell
python manage.py runserver 8001
```

La aplicación web estará disponible en:

```text
http://127.0.0.1:8001
```

Django consume los endpoints de FastAPI mediante `httpx` para obtener y mostrar la información de los productos.

## Arquitectura

```text
                 Navegador
                     │
                     ▼
              Django :8001
                     │
                  httpx
                     │
                     ▼
              FastAPI :8000
                     │
                     ▼
              MongoDB Atlas
```

De esta manera, **FastAPI** se encarga de la API y la comunicación con la base de datos, mientras que **Django** se encarga de la aplicación web y el renderizado de las plantillas.
