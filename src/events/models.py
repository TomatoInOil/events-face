import uuid

from django.db import models


class Place(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
    )


class Event(models.Model):
    class EventStatus(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
    )
    start_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=EventStatus.choices,
        default=EventStatus.OPEN,
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        related_name="events",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
