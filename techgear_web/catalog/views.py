import httpx
from django.shortcuts import render


def product_list(request):
    response = httpx.get("http://127.0.0.1:8000/products/")

    products = response.json()

    return render(request, "catalog/products.html", {
        "products": products
    })