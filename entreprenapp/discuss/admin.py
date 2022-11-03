from django.contrib import admin

from .models import ChatMessage, Room

admin.site.register(Room)
admin.site.register(ChatMessage)
