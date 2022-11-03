from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import ChatMessage, Room


class DiscussModelTests(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.admin_user = UserModel.objects.create_user(
            first_name="Bob",
            last_name="Zac",
            email="superuser@test.com",
            password="strongsecret123",
        )
        self.room = Room.objects.create(name="general")

    def test_create_room(self):
        room_data = {"name": "sales"}
        new_room = Room.objects.create(**room_data)
        self.assertEqual(new_room.name, room_data["name"])
        self.assertEqual(str(new_room), room_data["name"])

    def test_create_chat_message(self):
        """Create a chat messsage instance and check the properties data"""
        chat_message_data = {
            "room": self.room,
            "author": self.admin_user,
            "message": "Hello people",
            "date_time": timezone.now(),
        }

        chat_message = ChatMessage.objects.create(**chat_message_data)
        self.assertEqual(chat_message.room, chat_message_data["room"])
        self.assertEqual(chat_message.author, chat_message_data["author"])
        self.assertEqual(chat_message.message, chat_message_data["message"])
        self.assertEqual(
            chat_message.date_time, chat_message_data["date_time"]
        )
        self.assertEqual(
            str(chat_message),
            (
                f"R:{chat_message_data['room']} "
                f"U:{chat_message_data['author'].get_full_name()} "
                f"D:{chat_message_data['date_time']}"
            ),
        )
