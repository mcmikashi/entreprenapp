from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import ChatMessage, Room


class RoomChat(LoginRequiredMixin, TemplateView):
    template_name = "discuss/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] = get_object_or_404(Room, name=kwargs["room_name"])
        context["chat_messages"] = ChatMessage.objects.filter(
            room=context["room"]
        )
        return context
