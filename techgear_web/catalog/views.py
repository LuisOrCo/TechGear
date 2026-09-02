import os
import httpx
from django.shortcuts import render, redirect

FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://techgear-gepm.onrender.com")
LOCAL_FASTAPI_URL = "http://127.0.0.1:8000"


def fetch_api(method, path, **kwargs):
    """
    Realiza una petición HTTP a la API de FastAPI.
    Intenta primero la URL configurada (Render/Env) y si falla por RequestError,
    intenta con la URL local (http://127.0.0.1:8000) de respaldo.
    """
    timeout = kwargs.pop("timeout", 5.0)
    try:
        url = f"{FASTAPI_URL.rstrip('/')}{path}"
        return httpx.request(method, url, timeout=timeout, **kwargs)
    except httpx.RequestError:
        if FASTAPI_URL != LOCAL_FASTAPI_URL:
            try:
                url_local = f"{LOCAL_FASTAPI_URL}{path}"
                return httpx.request(method, url_local, timeout=timeout, **kwargs)
            except httpx.RequestError:
                pass
        raise


def product_list(request):
    products = []
    error = None

    try:
        response = fetch_api("GET", "/products/")
        if response.status_code == 200:
            products = response.json()
            for p in products:
                if "_id" in p and "id" not in p:
                    p["id"] = str(p["_id"])
        else:
            error = f"La API respondió con código de estado HTTP {response.status_code}."
    except httpx.RequestError:
        error = "No se pudo conectar con la API de FastAPI. Verifica que el servidor de la API esté iniciado."
    except Exception as e:
        error = f"Error inesperado al obtener productos: {str(e)}"

    return render(request, "catalog/products.html", {
        "products": products,
        "error": error,
        "active_tab": "catalog",
    })


def checkout(request, product_id=None):
    selected_product = None
    products = []
    error = None

    try:
        response = fetch_api("GET", "/products/")
        if response.status_code == 200:
            products = response.json()
            for p in products:
                if "_id" in p and "id" not in p:
                    p["id"] = str(p["_id"])
                if product_id and (str(p.get("id")) == str(product_id) or str(p.get("_id")) == str(product_id)):
                    selected_product = p
        else:
            error = f"Error al cargar productos desde la API (HTTP {response.status_code})."
    except httpx.RequestError:
        error = "No se pudo conectar con la API de FastAPI. Verifica que la API esté encendida."
    except Exception as e:
        error = f"Error al conectar con la API de productos: {str(e)}"

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        lastname = request.POST.get("lastname", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        post_product_id = request.POST.get("product_id") or product_id
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1

        if not selected_product and post_product_id:
            for p in products:
                if str(p.get("id")) == str(post_product_id) or str(p.get("_id")) == str(post_product_id):
                    selected_product = p
                    break

        if not selected_product:
            error = "Debe seleccionar un producto válido."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
                "active_tab": "catalog",
            })

        # Control de Excepción: Productos sin stock o cantidad excedida
        available_stock = int(selected_product.get("stock", 0))
        if available_stock <= 0:
            error = f"El producto '{selected_product.get('name')}' se encuentra totalmente agotado."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
                "active_tab": "catalog",
            })

        if quantity > available_stock:
            error = f"No hay suficiente stock para realizar este pedido (Stock disponible: {available_stock}, solicitado: {quantity})."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
                "active_tab": "catalog",
            })

        if not (name and lastname and email and phone and address):
            error = "Todos los campos del formulario de cliente son obligatorios."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
                "active_tab": "catalog",
            })

        unit_price = float(selected_product.get("price", 0))
        total = round(unit_price * quantity, 2)

        # 1. Registrar cliente en FastAPI (/customers/)
        customer_payload = {
            "name": name,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "address": address,
        }

        try:
            customer_resp = fetch_api("POST", "/customers/", json=customer_payload)
            if customer_resp.status_code not in (200, 201):
                detail = customer_resp.json().get("detail", "Error registrando el cliente")
                return render(request, "catalog/checkout.html", {
                    "products": products,
                    "selected_product": selected_product,
                    "error": f"Error al registrar cliente: {detail}",
                    "active_tab": "catalog",
                })
            created_customer = customer_resp.json()
            if isinstance(created_customer, dict):
                created_customer["id"] = str(created_customer.get("_id", created_customer.get("id", "")))
        except httpx.RequestError:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": "Servicio de Clientes no disponible (Servidor FastAPI caído).",
                "active_tab": "catalog",
            })
        except Exception as e:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": f"No se pudo registrar el cliente: {str(e)}",
                "active_tab": "catalog",
            })

        # 2. Registrar pedido en FastAPI (/orders/)
        order_payload = {
            "product_id": post_product_id,
            "quantity": quantity,
            "client_name": f"{name} {lastname}",
            "customer_email": email,
            "total": total,
        }

        try:
            order_resp = fetch_api("POST", "/orders/", json=order_payload)
            if order_resp.status_code not in (200, 201):
                detail = order_resp.json().get("detail", "Error creando el pedido")
                return render(request, "catalog/checkout.html", {
                    "products": products,
                    "selected_product": selected_product,
                    "error": f"Error al crear el pedido: {detail}",
                    "active_tab": "catalog",
                })
            created_order = order_resp.json()
            if isinstance(created_order, dict):
                created_order["id"] = str(created_order.get("_id", created_order.get("id", "")))
        except httpx.RequestError:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": "Servicio de Pedidos no disponible (Servidor FastAPI caído).",
                "active_tab": "catalog",
            })
        except Exception as e:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": f"No se pudo crear el pedido: {str(e)}",
                "active_tab": "catalog",
            })

        return render(request, "catalog/order_success.html", {
            "customer": created_customer,
            "order": created_order,
            "product": selected_product,
            "quantity": quantity,
            "total": total,
            "active_tab": "catalog",
        })

    return render(request, "catalog/checkout.html", {
        "products": products,
        "selected_product": selected_product,
        "error": error,
        "active_tab": "catalog",
    })


def admin_panel(request):
    products = []
    error = None

    try:
        response = fetch_api("GET", "/products/")
        if response.status_code == 200:
            products = response.json()
            for p in products:
                if "_id" in p and "id" not in p:
                    p["id"] = str(p["_id"])
        else:
            error = f"Error al obtener productos desde la API (HTTP {response.status_code})."
    except httpx.RequestError:
        error = "No se pudo conectar con la API de FastAPI. Verifica que el servidor de la API esté iniciado."
    except Exception as e:
        error = f"Error inesperado al obtener productos: {str(e)}"

    return render(request, "catalog/admin_panel.html", {
        "products": products,
        "error": error,
        "active_tab": "admin",
    })


def product_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "").strip()

        try:
            price = float(request.POST.get("price", 0))
            stock = int(request.POST.get("stock", 0))
        except ValueError:
            price = 0
            stock = 0

        if name and description and category and price > 0 and stock >= 0:
            payload = {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category": category,
            }

            try:
                fetch_api("POST", "/products/", json=payload)
            except Exception as e:
                print(f"Error al crear producto: {e}")

    return redirect("admin_panel")


def product_edit(request, product_id):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "").strip()

        try:
            price = float(request.POST.get("price", 0))
            stock = int(request.POST.get("stock", 0))
        except ValueError:
            price = 0
            stock = 0

        if name and description and category and price > 0 and stock >= 0:
            payload = {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category": category,
            }

            try:
                fetch_api("PUT", f"/products/{product_id}", json=payload)
            except Exception as e:
                print(f"Error al editar producto: {e}")

    return redirect("admin_panel")


def product_delete(request, product_id):
    if request.method == "POST":
        try:
            fetch_api("DELETE", f"/products/{product_id}")
        except Exception as e:
            print(f"Error al eliminar producto: {e}")

    return redirect("admin_panel")


def orders_list(request):
    orders = []
    error = None

    try:
        response = fetch_api("GET", "/orders/")
        if response.status_code == 200:
            orders = response.json()
            for o in orders:
                if "_id" in o and "id" not in o:
                    o["id"] = str(o["_id"])
        else:
            error = f"Error al consultar la lista de pedidos desde la API (HTTP {response.status_code})."
    except httpx.RequestError:
        error = "No se pudo conectar con la API de FastAPI. Verifica que el servidor de la API esté iniciado."
    except Exception as e:
        error = f"Error inesperado al obtener pedidos: {str(e)}"

    return render(request, "catalog/orders_list.html", {
        "orders": orders,
        "error": error,
        "active_tab": "orders",
    })


def order_detail(request, order_id):
    order = None
    product = None
    error = None

    try:
        response = fetch_api("GET", f"/orders/{order_id}")
        if response.status_code == 200:
            order = response.json()
            if "_id" in order and "id" not in order:
                order["id"] = str(order["_id"])

            product_id = order.get("product_id")
            if product_id:
                try:
                    prod_resp = fetch_api("GET", f"/products/{product_id}")
                    if prod_resp.status_code == 200:
                        product = prod_resp.json()
                        if "_id" in product and "id" not in product:
                            product["id"] = str(product["_id"])
                except Exception:
                    pass
        else:
            error = f"No se encontró el pedido con ID '{order_id}' (HTTP {response.status_code})."
    except httpx.RequestError:
        error = "No se pudo conectar con la API de FastAPI."
    except Exception as e:
        error = f"Error al cargar el detalle del pedido: {str(e)}"

    return render(request, "catalog/order_detail.html", {
        "order": order,
        "product": product,
        "error": error,
        "active_tab": "orders",
    })