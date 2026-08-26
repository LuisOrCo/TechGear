# TechGear

TechGear es una tienda especializada en hardware y accesorios tecnológicos. El proyecto utiliza una API desarrollada con **FastAPI** para gestionar productos, clientes y pedidos en una base de datos **MongoDB Atlas**, junto con una aplicación web desarrollada con **Django** para renderizar la interfaz de usuario desde el servidor (MVT).

## Tecnologías

* **Python**
* **FastAPI** — API Backend
* **Django** — Aplicación Web / MVT
* **MongoDB Atlas** — Base de datos NoSQL (`productos`, `clientes`, `pedidos`)
* **httpx** — Consumo de la API desde Django
* **Uvicorn** — Servidor de desarrollo ASGI para FastAPI

---

## Estructura del proyecto

```text
TechGear/
│
├── techgear_api/                       # API Backend (FastAPI)
│   ├── app/
│   │   ├── database/                   # Configuración y conexión a MongoDB
│   │   │   ├── __init__.py
│   │   │   └── connection.py
│   │   │
│   │   ├── routes/                     # Endpoints de la API
│   │   │   ├── __init__.py
│   │   │   ├── customer.py             # Endpoints /customers/
│   │   │   ├── order.py                # Endpoints /orders/
│   │   │   └── product.py              # Endpoints /products/
│   │   │
│   │   ├── schemas/                    # Modelos Pydantic (Validación)
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── order.py
│   │   │   └── product.py
│   │   │
│   │   ├── services/                   # Lógica de negocio e interacción con MongoDB
│   │   │   ├── __init__.py
│   │   │   ├── customer_service.py
│   │   │   ├── order_service.py
│   │   │   └── product_service.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py                     # Punto de entrada de FastAPI
│   │
│   └── .env                            # Variables de entorno (MongoDB URL)
│
├── techgear_web/                       # Aplicación Web (Django)
│   ├── catalog/
│   │   ├── migrations/
│   │   ├── templates/                  # Plantillas HTML
│   │   │   └── catalog/
│   │   │       ├── checkout.html       # Formulario de cliente y checkout
│   │   │       ├── order_success.html  # Resumen y confirmación de pedido
│   │   │       └── products.html       # Catálogo de productos
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py                    # Vistas y consumo HTTP con httpx
│   │
│   ├── config/                         # Configuración del proyecto Django
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

---

## Manejo de Excepciones

El proyecto implementa un control de excepciones robusto tanto en la API (FastAPI) como en la aplicación web (Django):

1. **API Caída (Error de conexión HTTP)**:
   - Django captura los errores de conexión (`httpx.RequestError`) si el servidor de FastAPI no se encuentra en ejecución o inalcanzable.
   - En lugar de colapsar la aplicación con un error 500, Django muestra mensajes de alerta amigables en las plantillas HTML indicando al usuario que el servicio de API no está disponible temporalmente.

2. **Control de Stock en Productos**:
   - **En Django**: La vista de `checkout` valida que el producto seleccionado tenga stock disponible (`stock > 0`) y que la cantidad solicitada no exceda las existencias en inventario.
   - **En FastAPI**: El servicio `create_order` verifica en MongoDB que el producto exista y cuente con stock suficiente. Si el producto está agotado o no tiene stock para la cantidad pedida, la API responde con un código de estado `HTTP 400 Bad Request` indicando la razón exacta.
   - **Descuento Automático de Inventario**: Al confirmarse exitosamente una orden en FastAPI, se descuenta automáticamente la cantidad comprada de la colección `productos`.

3. **Validación de Datos en Formularios**:
   - Pydantic valida que los correos electrónicos sean válidos (`EmailStr`), que los teléfonos tengan el formato adecuado y que los nombres cumplan con la longitud requerida antes de guardar en la colección `clientes`.

---

## Instalación y Configuración

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd TechGear
   ```

2. Crear y activar el entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecutar el Backend (FastAPI)

1. Acceder a la carpeta `techgear_api`:
   ```powershell
   cd techgear_api
   ```

2. Iniciar el servidor Uvicorn:
   ```powershell
   ..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
   ```

   - API Base: `http://127.0.0.1:8000`
   - Documentación Interactiva Swagger: `http://127.0.0.1:8000/docs`

---

## Ejecutar el Frontend (Django)

1. En una segunda terminal con el entorno virtual activo, acceder a la carpeta `techgear_web`:
   ```powershell
   cd techgear_web
   ```

2. Iniciar el servidor de desarrollo de Django en el puerto 8001:
   ```powershell
   ..\venv\Scripts\python.exe manage.py runserver 8001
   ```

   - Catálogo Web: `http://127.0.0.1:8001/products/`

---

## Arquitectura del Sistema

```text
                  Navegador Web
                       │
                       ▼
                Django :8001 (MVT / HTML Templates)
                       │
                     httpx
                       │
                       ▼
                FastAPI :8000 (REST API / Pydantic)
                       │
                       ▼
                MongoDB Atlas (`productos`, `clientes`, `pedidos`)
```

---

## URL del Deploy de la API

```text
https://techgear-gepm.onrender.com
```