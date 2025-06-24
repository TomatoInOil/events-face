import rest_framework.serializers

from src.events.models import Event


class EventSerializer(rest_framework.serializers.ModelSerializer):
    place = rest_framework.serializers.CharField(source="place.name", read_only=True)

    class Meta:
        model = Event
        fields = ("id", "name", "start_date", "status", "place")
