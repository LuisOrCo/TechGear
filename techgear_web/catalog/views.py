import httpx
from django.shortcuts import render

FASTAPI_URL = "http://127.0.0.1:8000"


def product_list(request):
    products = []
    error = None

    try:
        response = httpx.get(f"{FASTAPI_URL}/products/", timeout=5.0)
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
    })


def checkout(request, product_id=None):
    selected_product = None
    products = []
    error = None

    try:
        response = httpx.get(f"{FASTAPI_URL}/products/", timeout=5.0)
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
        error = "No se pudo conectar con la API de FastAPI. Verifica que la API esté encendida en http://127.0.0.1:8000."
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
            })

        # Control de Excepción: Productos sin stock o cantidad excedida
        available_stock = int(selected_product.get("stock", 0))
        if available_stock <= 0:
            error = f"El producto '{selected_product.get('name')}' se encuentra totalmente agotado."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
            })

        if quantity > available_stock:
            error = f"No hay suficiente stock para realizar este pedido (Stock disponible: {available_stock}, solicitado: {quantity})."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
            })

        if not (name and lastname and email and phone and address):
            error = "Todos los campos del formulario de cliente son obligatorios."
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": error,
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
            customer_resp = httpx.post(f"{FASTAPI_URL}/customers/", json=customer_payload, timeout=5.0)
            if customer_resp.status_code not in (200, 201):
                detail = customer_resp.json().get("detail", "Error registrando el cliente")
                return render(request, "catalog/checkout.html", {
                    "products": products,
                    "selected_product": selected_product,
                    "error": f"Error al registrar cliente: {detail}",
                })
            created_customer = customer_resp.json()
            if isinstance(created_customer, dict):
                created_customer["id"] = str(created_customer.get("_id", created_customer.get("id", "")))
        except httpx.RequestError:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": "Servicio de Clientes no disponible (Servidor FastAPI caído).",
            })
        except Exception as e:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": f"No se pudo registrar el cliente: {str(e)}",
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
            order_resp = httpx.post(f"{FASTAPI_URL}/orders/", json=order_payload, timeout=5.0)
            if order_resp.status_code not in (200, 201):
                detail = order_resp.json().get("detail", "Error creando el pedido")
                return render(request, "catalog/checkout.html", {
                    "products": products,
                    "selected_product": selected_product,
                    "error": f"Error al crear el pedido: {detail}",
                })
            created_order = order_resp.json()
            if isinstance(created_order, dict):
                created_order["id"] = str(created_order.get("_id", created_order.get("id", "")))
        except httpx.RequestError:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": "Servicio de Pedidos no disponible (Servidor FastAPI caído).",
            })
        except Exception as e:
            return render(request, "catalog/checkout.html", {
                "products": products,
                "selected_product": selected_product,
                "error": f"No se pudo crear el pedido: {str(e)}",
            })

        return render(request, "catalog/order_success.html", {
            "customer": created_customer,
            "order": created_order,
            "product": selected_product,
            "quantity": quantity,
            "total": total,
        })

    return render(request, "catalog/checkout.html", {
        "products": products,
        "selected_product": selected_product,
        "error": error,
    })