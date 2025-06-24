from django.urls import path

from src.events.views import EventList

app_name = "events"

urlpatterns = [
    path("events/", EventList.as_view(), name="event-list"),
]
