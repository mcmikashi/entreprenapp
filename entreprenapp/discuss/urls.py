from django.urls import path

from .views import RoomChat

app_name = "discuss"

urlpatterns = [
    path("<str:room_name>", RoomChat.as_view(), name="room"),
]
