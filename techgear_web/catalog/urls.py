from django.urls import path
from .views import product_list, checkout

urlpatterns = [
    path("", product_list, name="product_list"),
    path("products/", product_list),
    path("checkout/<str:product_id>/", checkout, name="checkout"),
    path("checkout/", checkout, name="checkout"),
]