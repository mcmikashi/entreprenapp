import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import ChatMessage, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "author_id": self.user.id,
                "author_full_name": self.user.get_full_name(),
                "date_time": now.isoformat(),
            },
        )
        # Store the message on the database
        room = sync_to_async(get_object_or_404)(
            Room, name=self.room_group_name[5:]
        )
        chat_message = sync_to_async(ChatMessage.objects.create)(
            room=await room, author=self.user, message=message, date_time=now
        )

        await chat_message

    # Receive message from room group
    async def chat_message(self, event):
        # Send the data to WebSocket
        await self.send(text_data=json.dumps({**event}))
