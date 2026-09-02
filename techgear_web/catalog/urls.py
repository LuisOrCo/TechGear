from django.urls import path
from .views import (
    product_list,
    checkout,
    admin_panel,
    product_create,
    product_edit,
    product_delete,
    orders_list,
    order_detail,
)

urlpatterns = [
    path("", product_list, name="product_list"),
    path("products/", product_list),
    path("checkout/<str:product_id>/", checkout, name="checkout"),
    path("checkout/", checkout, name="checkout"),
    path("admin-panel/", admin_panel, name="admin_panel"),
    path("admin-panel/product/create/", product_create, name="product_create"),
    path("admin-panel/product/edit/<str:product_id>/", product_edit, name="product_edit"),
    path("admin-panel/product/delete/<str:product_id>/", product_delete, name="product_delete"),
    path("orders/", orders_list, name="orders_list"),
    path("orders/<str:order_id>/", order_detail, name="order_detail"),
]