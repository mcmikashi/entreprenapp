from django.urls import path

from .views import (
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
]
