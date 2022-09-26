from django.urls import path
from .views import (
    CustomLoginView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetCompleteView,
)

from django.contrib.auth.views import logout_then_login

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout", logout_then_login, name="logout"),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset_confirm//<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
