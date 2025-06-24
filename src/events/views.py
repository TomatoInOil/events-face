import rest_framework.generics

from src.events.models import Event
from src.events.serializers import EventSerializer


class EventList(rest_framework.generics.ListAPIView):
    queryset = (
        Event.objects.select_related("place")
        .filter(status=Event.EventStatus.OPEN)
        .all()
    )
    serializer_class = EventSerializer
    filterset_fields = ["name"]
