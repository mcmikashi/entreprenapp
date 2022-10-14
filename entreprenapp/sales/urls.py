from django.urls import path

from .views import (
    CustomerCreateView,
    CustomerDeleteView,
    CustomerListView,
    CustomerUpdateView,
    EstimateCreateView,
    EstimateDeleteView,
    EstimateDetailView,
    EstimateListView,
    EstimatePDFView,
    EstimateUpdateView,
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
    path(
        "estimate/create/",
        EstimateCreateView.as_view(),
        name="estimate_create",
    ),
    path(
        "estimate/pdf/<int:pk>",
        EstimatePDFView.as_view(),
        name="estimate_pdf",
    ),
    path(
        "estimate/delete/<int:pk>",
        EstimateDeleteView.as_view(),
        name="estimate_delete",
    ),
    path(
        "estimate/update/<int:pk>",
        EstimateUpdateView.as_view(),
        name="estimate_update",
    ),
    path(
        "estimate/list/",
        EstimateListView.as_view(),
        name="estimate_list",
    ),
    path(
        "estimate/detail/<int:pk>",
        EstimateDetailView.as_view(),
        name="estimate_detail",
    ),
    path(
        "estimate/update/<int:pk>",
        EstimateUpdateView.as_view(),
        name="estimate_update",
    ),
]
