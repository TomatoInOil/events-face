import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from src.events.models import Event, Place


class Command(BaseCommand):
    help = "Generate dummy data for the events app"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        if options["clear"]:
            Place.objects.all().delete()
            Event.objects.all().delete()

        count = options["count"]
        places = [Place.objects.create(name=f"Place {i}") for i in range(count)]
        places.append(None)
        for i in range(count):
            place = random.choice(places)
            Event.objects.create(
                name=f"Event {i}",
                start_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                status=random.choice(Event.EventStatus.choices)[0],
                place=place,
            )

        self.stdout.write(f"Successfully generated {count} events and {count} places")
