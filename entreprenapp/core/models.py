from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Core(models.Model):
    is_active = models.BooleanField(_("is active"), default=True)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_create",
        blank=True,
        null=True,
    )
    modified_date = models.DateTimeField(
        _("modified date"), auto_now=True, blank=True, null=True
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("modified by"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_update",
    )
    deleted_date = models.DateTimeField(
        _("deleted date"), blank=True, null=True
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("deleted by"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_delete",
    )

    class Meta:
        abstract = True
