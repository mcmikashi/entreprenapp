from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):

    name = models.SlugField(_("name"), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class ChatMessage(models.Model):
    """Model definition for Chat Message."""

    room = models.ForeignKey(
        "discuss.Room", verbose_name=_("Room"), on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    message = models.CharField(max_length=255)
    date_time = models.DateTimeField(_("date and time"))

    def __str__(self):
        return (
            f"R:{self.room} U:{self.author.get_full_name()} D:{self.date_time}"
        )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
