from django.contrib import admin

from .models import Event, Place


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "status", "place")
    list_filter = ("status",)
    search_fields = ("name",)
    list_editable = ("status",)
    list_per_page = 50
    list_max_show_all = 100


class EventInline(admin.TabularInline):
    model = Event
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [
        EventInline,
    ]
    search_fields = ("name",)
    list_per_page = 50
    list_max_show_all = 100
