from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerListView,
    CustomerUpdateView,
    ItemCreateView,
    ItemDeleteView,
    ItemListView,
    ItemUpdateView,
    SalerCreateView,
    SalerDeleteView,
    SalerListView,
    SalerUpdateView,
)

app_name = "sales"

urlpatterns = [
    path("saler/list/", SalerListView.as_view(), name="saler_list"),
    path("saler/create/", SalerCreateView.as_view(), name="saler_create"),
    path(
        "saler/update/<int:pk>/",
        SalerUpdateView.as_view(),
        name="saler_update",
    ),
    path(
        "saler/delete/<int:pk>/",
        SalerDeleteView.as_view(),
        name="saler_delete",
    ),
    path("customer/list/", CustomerListView.as_view(), name="customer_list"),
    path(
        "customer/create/",
        CustomerCreateView.as_view(),
        name="customer_create",
    ),
    path(
        "customer/update/<int:pk>/",
        CustomerUpdateView.as_view(),
        name="customer_update",
    ),
    path(
        "customer/delete/<int:pk>/",
        CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
    path("item/list/", ItemListView.as_view(), name="item_list"),
    path(
        "item/create/",
        ItemCreateView.as_view(),
        name="item_create",
    ),
    path(
        "item/update/<int:pk>/",
        ItemUpdateView.as_view(),
        name="item_update",
    ),
    path(
        "item/delete/<int:pk>/",
        ItemDeleteView.as_view(),
        name="item_delete",
    ),
]
