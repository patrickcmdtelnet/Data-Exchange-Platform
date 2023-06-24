from django.db import models
from django.utils import timezone


class DateTimeStampMixin(models.Model):
    """
    Model mixin that provides timestamping fields.
    """

    created_date = models.DateTimeField("date created", default=timezone.now)
    updated_date = models.DateTimeField(
        "date updated", auto_now_add=True, null=True, blank=True
    )

    class Meta:
        abstract = True
        ordering = ["created_date"]
